# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 13:44:06 2015
This file is part of pyNLO.

    pyNLO is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyNLO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyNLO.  If not, see <http://www.gnu.org/licenses/>.
@author: ycasg
"""

import numpy as np
from scipy.interpolate import interp1d
from pynlo.media.fibers.calculators import DTabulationToBetas
from scipy.misc import factorial
from scipy import constants
from scipy.optimize import minimize
from pynlo.util.pynlo_ffts import IFFT_t
from pynlo.media.fibers import JSONFiberLoader


#fiber:
#    "name"
#    "dispersion_format" ["D","GVD"]
#    "nonlinear_parameter"
#    if D:
#        "dispersion_x_units"
#        "dispersion_y_units"
#        "dispersion_data" [2,n]
#    if GVD:
#        "dispersion_gvd_units"
#        "dispersion_gvd_center_wavelength"
#        "dispersion_data"[1,n]
#    "is_gain"
#    if is_gain:
#        "gain_spectrum"
#        "gain_x_units"

class FiberInstance:
    """This is a class that contains the information about a fiber."""
    betas       = None
    length      = None
    fibertype   = None
    fiberspecs  = {}
    poly_order  = None
    gamma       = None
    def __init__(self):
        self.c_mks = constants.speed_of_light
        self.c = constants.speed_of_light * 1e9/1e12 # c in nm/ps
        self.is_simple_fiber = False
        self.fiberloader = JSONFiberLoader.JSONFiberLoader('nist_fibers')
        self.dispersion_changes_with_z = False
        
        
    def load_from_db(self, length, fibertype, poly_order = 2):
        """This loads a fiber from the database. """
        self.fibertype = fibertype
        self.fiberspecs = self.fiberloader.get_fiber(fibertype)
        self.length = length
        self.betas = np.array([0])
        self.gamma = self.fiberspecs["gamma"]
        self.poly_order = poly_order
        self.load_dispersion()
    
    def load_from_file(self, filename, length=0.1, fiberName=None, gamma_W_m=0, gain=0,
                       alpha=0, delimiter=',', skiprows=0, poly_order=3):
        """
        This loads dispersion give the path of a file. 
        The file is expected to be in the format
        wavelength (nm), D (ps/nm/km).
        """
        import os
        
        if fiberName == None:
            self.fibertype = os.path.basename(filename)
        else:
            self.fibertype = fiberName
        
        self.fiberspecs["dispersion_format"] = "D"
        self.poly_order = poly_order
        self.gain       = gain
        self.length     = length
        self.gamma      = gamma_W_m
        
        if gain == 0:
            self.fiberspecs["is_gain"] = False
        else:
            self.fiberspecs["is_gain"] = True

        self.fiberspecs['gain_x_data' ] = None
        
        self.x, self.y = np.loadtxt(filename, delimiter=delimiter, skiprows=skiprows, unpack=True)
            
    def load_dispersion(self):
        """This is typically called by the "load_from_db" function. 
        It takes the values from the self.fiberspecs dict and transfers them into the appropriate variables. """
        if self.fiberspecs["dispersion_format"] == "D":
            self.dispersion_x_units = self.fiberspecs["dispersion_x_units"]
            self.dispersion_y_units = self.fiberspecs["dispersion_y_units"]
            self.x = self.fiberspecs["dispersion_x_data"]
            self.y = self.fiberspecs["dispersion_y_data"]
            return 1
        elif self.fiberspecs["dispersion_format"] == "GVD":
            self.dispersion_gvd_units = self.fiberspecs["dispersion_gvd_units"]
            self.center_wavelength = self.fiberspecs["dispersion_gvd_center_wavelength"]
            # If in km^-1 units, scale to m^-1
            if self.dispersion_gvd_units == 'ps^n/km':
                self.betas = np.array(self.fiberspecs["dispersion_data"]) / 1e3
            return 1
        else:
            print "Error: no dispersion found."
            return None
    
    def set_dispersion_function(self, dispersion_function, dispersion_format='GVD'):
        """
        This allows the user to provide a function for the fiber dispersion that can vary as a function
        of `z`, the lenght along the fiber. The function can either provide beta2, beta3, beta4, etc. 
        coefficients, or provide two arrays, wavelength (nm) and D (ps/nm/km)
        
        Parameters
        ----------
        dispersion_function : function 
            returning D or Beta coefficients as a function of z
        dispersion_formats: 'GVD' or 'D'
            determines if the dispersion will be identified in terms of Beta coefficients 
            (GVD, in units of ps^2/m, not ps^2/km) or
            D (ps/nm/km)
        
        Notes
        -----
        For example, this code will create a fiber where Beta2 changes from anomalous
        to zero along the fiber: ::
        
            Length = 1.5 
            
            def myDispersion(z):
                
                frac = 1 - z/(Length)
                
                beta2 = frac * -50e-3
                beta3 = 0
                beta4 = 1e-7
    
                return beta2, beta3, beta4

        
        fiber1 = fiber.FiberInstance()
        fiber1.generate_fiber(Length, center_wl_nm=800, betas=myDispersion(0), gamma_W_m=1)
        
        
        fiber.set_dispersion_function(myDisperion, dispersion_format='GVD')
        """
        
        self.dispersion_changes_with_z = True
        self.fiberspecs["dispersion_format"] = dispersion_format
        self.dispersion_function = dispersion_function
        
        
    def get_betas(self, pulse, z=0):
        """This provides the propagation constant (beta) at the frequencies of the supplied pulse grid.
        The units are 1/meters. 
        
        Two different methods are used, 
        
        If fiberspecs["dispersion_format"] == "D", then the DTabulationToBetas function is used to
        fit the datapoints in terms of the Beta2, Beta3, etc. coefficients expanded around the pulse 
        central frequency. 
        
        If fiberspecs["dispersion_format"] == "GVD", then the betas are calculated as a Taylor expansion
        using the Beta2, Beta3, etc. coefficients around the *fiber* central frequency. 
        However, since this expansion is done without the lower order coefficients, the first two 
        terms of the Taylor expansion are not defined. In order to provide a nice input for the SSFM,
        which assumes that the group velocity will be zero at the pulse central frequency,
        the slope and offset at the pump central frequency are set to zero. 
        
        Parameters
        ----------
        pulse : an instance of the :class:`pynlo.light.pulse.PulseBase` class
            the pulse must be supplied in order for the frequency grid to be known
        
        
        Returns
        -------
        B : 1D array of floats
            the propagation constant (beta) at the frequency gridpoints of the supplied pulse
            (units of 1/meters).
        
        """
        
        if self.dispersion_changes_with_z:
            if self.fiberspecs["dispersion_format"] == "D":
                self.x, self.y = self.dispersion_function(z)
            if self.fiberspecs["dispersion_format"] == "GVD":
                self.betas     = np.array(self.dispersion_function(z))
            
        B = np.zeros((pulse.NPTS,))
        if self.fiberspecs["dispersion_format"] == "D":
            self.betas = DTabulationToBetas(pulse.center_wavelength_nm,
                                            np.transpose(np.vstack((self.x,self.y))),
                                            self.poly_order,
                                            DDataIsFile = False)
            for i in range(len(self.betas)):
                B = B + self.betas[i]/factorial(i+2)*pulse.V_THz**(i+2)
            return B
            
        elif self.fiberspecs["dispersion_format"] == "GVD":
            # calculate beta[n]/n! * (w-w0)^n
            # w0 is the center of the Taylor expansion, and is defined by the
            # fiber. the w's are from the optical spectrum
            fiber_omega0 =  2*np.pi*self.c / self.center_wavelength # THz
            betas = self.betas
            for i in range(len(betas)):
                betas[i] = betas[i]
                B = B + betas[i] / factorial(i + 2) * (pulse.W_THz-fiber_omega0)**(i + 2)
            
            # now we have beta calculated in terms of distance from the fiber central frequency
            # what we want is to have beta referenced from the *pulse* central frequency
                
            center_index = np.argmin(np.abs(pulse.V_THz))
            slope = np.gradient(B)/np.gradient(pulse.W_THz)
            B = B - slope[center_index] * (pulse.V_THz) - B[center_index]
            
            return B
            
        else:
            return -1
    def get_gain(self,pulse,output_power = 1):
        """ Retrieve gain spectrum for fiber. If fiber has 'simple gain', this
        is a scalar. If the fiber has a gain spectrum (eg EDF or YDF), this will
        return this spectrum as a vector corresponding to the Pulse class
        frequency axis. In this second case, the output power must be specified, from
        which the gain/length is calculated. """
        if self.fiberspecs["is_gain"]:
            if self.is_simple_fiber:
                return self.gain
            else:
                # If the fiber is generated then it has no gain spectrum
                # and an array with all values equal to self.gain is returned.
                # This is signaled by gain_x_data.
                if self.fiberspecs['gain_x_data'] is not None:
                    self.gain_x_units = self.fiberspecs["gain_x_units"]
                    x = np.array(self.fiberspecs["gain_x_data"])
                    y = np.array(self.fiberspecs["gain_y_data"])
                    f = interp1d(self.c_mks/x[::-1],y[::-1],kind ='cubic',
                                 bounds_error=False,fill_value=0)
                    gain_spec = f(pulse.W_mks/ (2*np.pi))

                    g = lambda k: np.abs(output_power - pulse.frep_Hz * pulse.dT_mks*
                                        np.trapz(np.abs(
                                            IFFT_t( pulse.AW *
                                                np.exp(k*gain_spec*self.length/2.0)
                                                )
                                                )**2))

                    scale_factor = minimize(g, 1, method='Powell')
#                    print 'Power:',pulse.frep * pulse.dt_seconds*\
#                                        np.trapz(np.abs(
#                                            IFFT_t( FFT_t(pulse.A) *
#                                                np.exp(scale_factor.x*gain_spec*self.length/2.0)
#                                                )
#                                                )**2)
                    return gain_spec * scale_factor.x
                else:
                    return np.ones((pulse.NPTS,)) * self.gain
        else:
            return np.zeros((pulse.NPTS,))

    def Beta2_to_D(self, pulse): # in ps / nm / km
        """ This provides the dispersion parameter D (in ps / nm / km) at each frequency of the supplied pulse"""
        return -2 * np.pi * self.c / pulse.wl_nm**2 * self.Beta2(pulse) * 1000
    def Beta2(self, pulse):
        """ This provides the beta_2 (in ps^2 / meter)."""
        dw = pulse.V_THz[1] - pulse.V_THz[0]
        out = np.diff(self.get_betas(pulse), 2) / dw**2
        out = np.append(out[0], out)
        out = np.append(out, out[-1])
        return out

    def generate_fiber(self, length, center_wl_nm, betas, gamma_W_m, gain = 0,
                       gvd_units = 'ps^n/m', label = 'Simple Fiber'):
        """ This generates a fiber instance using the beta-coefficients."""
        
        self.length = length
        self.fiberspecs= {}
        self.fiberspecs['dispersion_format'] = 'GVD'
        self.fibertype = label
        if gain == 0:
            self.fiberspecs["is_gain"] = False
        else:
            self.fiberspecs["is_gain"] = True
        self.gain = gain
        # The following line signals get_gain to use a flat gain spectrum
        self.fiberspecs['gain_x_data' ] = None

        self.center_wavelength = center_wl_nm
        self.betas = np.copy(np.array(betas))
        self.gamma = gamma_W_m
        # If in km^-1 units, scale to m^-1
        if gvd_units == 'ps^n/km':
            self.betas = self.betas * 1.0e-3