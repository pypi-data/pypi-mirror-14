# Copyright 2014-2016 The ODL development group
#
# This file is part of ODL.
#
# ODL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ODL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ODL.  If not, see <http://www.gnu.org/licenses/>.

"""Using the FT to define a convolution."""

# Imports for common Python 2/3 codebase
from __future__ import print_function, division, absolute_import
from future import standard_library
standard_library.install_aliases()

import numpy as np

from odl.operator.operator import Operator
import odl


_SUPPORTED_IMPL = ('numpy_ft', 'numpy_dft', 'pyfftw_ft', 'pyfftw_dft')
_SUPPORTED_KER_MODES = ('real', 'ft', 'dft', 'ft_hc', 'dft_hc')


class Convolution(Operator):

    """Discretized convolution operator.

    The continuous convolution of two functions ``f`` and ``g`` on R is
    defined as::

        Conv(f, g)(x) = integrate_R ( f(x - y) * g(y) dy )

    With the help of the Fourier transform, this operator can be written
    as a multiplication::

        FT[Conv(f, g)] = sqrt(2 pi) FT(f) * FT(g)

    If one of the functions is fixed, say ``g``, then the convolution is
    a mapping from ``L^p(R)`` to itself (provided ``g in L^1(R)``.
    """

    def __init__(self, dom, ran=None, kernel=None, **kwargs):
        """Initialize a new instance.

        Parameters
        ----------
        dom : `DiscreteLp` or `ProductSpace` with 2 parts
            Domain of the operator. If a `DiscreteLp` is given, a
            ``kernel`` or ``kernel_ft`` must be specified.
        ran : `DiscreteLp`, optional
            Range of the operator, by default the same as ``dom`` or
            ``dom[0]``, resp.
        kernel : optional
            Needs to be specified if ``dom`` is a `DiscreteLp` instance.
            The kernel can be specified in a variety of ways:

            domain `element-like` : Any object that can be turned into
            an element of ``dom``, i.e. a vectorized function, an
            array of correct shape or a `DiscreteLpVector`

            `element-like` for the range of `FourierTransform` defined
            on ``dom`` : Like above, but the object is interpreted as
            the Fourier transform of a real-space kernel. The correct
            space can be calculated with `reciprocal_space`

            `element-like` for the range of `DiscreteFourierTransform`
             defined on ``dom`` : Like above, but the values are
             interpreted as the result of the pure DFT instead. This
             method is faster but assumes periodic functions.

        impl : `str`, optional
            Implementation of the convolution. Available options are:

            'numpy_ft' : Fourier transform using Numpy FFT (default)

            'numpy_dft' : Discrete FT using Numpy FFT

            'pyfftw_ft' : Fourier transform using pyFFTW

            'pyfftw_dft' : Discrete Fourier transform using pyFFTW

        kernel_mode : {'real', 'ft', 'dft'}, optional
            How the provided kernel is to be interpreted:

            'real' : element of ``dom`` (default)

            'ft' : function in the range of the Fourier transform

            'ft_hc' : function in the range of the half-complex
            (real-to-complex) Fourier transform

            'dft' : discrete array in the range of the Discrete FT

            'dft_hc' : discrete array in the range of the half-complex
            (real-to-complex) Discrete FT

        axes : sequence of `int`, optional
            Dimensions in which to convolve. Default: all axes

        cache_ker_ft : `bool`, optional
            If `True`, the Fourier transform (or DFT) of the kernel is
            stored during the first evaluation.
            Default: `False`

        See also
        --------
        FourierTransform : discretization of the continuous FT
        DiscreteFourierTransform : "pure", trigonometric sum DFT
        """
        # TODO: better factor out into an own class BilinearConvolution
        if isinstance(dom, odl.DiscreteLp):
            dom_is_product = False
        elif (isinstance(dom, odl.ProductSpace) and
              all(isinstance(s, odl.DiscreteLp) for s in dom)):
            dom_is_product = True
        else:
            raise TypeError('domain {!r} is neither a DiscreteLp instance '
                            'nor a product space of such.'.format(dom))

        if ran is not None:
            raise NotImplementedError('custom range not implemented')
        else:
            ran = dom[0] if dom_is_product else dom

        super().__init__(dom, ran, linear=not dom_is_product)

        if not dom_is_product and kernel is None:
            raise ValueError('kernel must be specified if the domain is not '
                             'a product space.')

        impl = kwargs.pop('impl', 'numpy_ft')
        impl, impl_in = str(impl).lower(), impl
        if impl not in _SUPPORTED_IMPL:
            raise ValueError("implementation '{}' not understood."
                             ''.format(impl_in))
        self._impl = impl

        ker_mode = kwargs.pop('kernel_mode', 'real')
        ker_mode, ker_mode_in = str(ker_mode).lower(), ker_mode
        if ker_mode not in _SUPPORTED_KER_MODES:
            raise ValueError("kernel mode '{}' not understood."
                             ''.format(ker_mode_in))

        self._kernel_mode = ker_mode

        use_ft = (impl in ('numpy_ft', 'pyfftw_ft'))
        use_dft = (impl in ('numpy_dft', 'pyfftw_dft'))

        if not (use_ft or use_dft) and ker_mode != 'real':
            raise ValueError("kernel mode 'real' is required for non-FT "
                             "based convolutions.")

        axes = kwargs.pop('axes', list(range(self.domain.ndim)))
        if ker_mode == 'real':
            halfcomplex = True  # use default depending on domain
        else:
            halfcomplex = ker_mode.endswith('hc')

        fft_impl = self.impl.split('_')[0]

        if use_ft:
            self._transform = odl.trafos.FourierTransform(
                self.domain, axes=axes, halfcomplex=halfcomplex,
                impl=fft_impl)
            self._factor = np.sqrt(2 * np.pi) ** self.domain.ndim
        elif use_dft:
            self._transform = odl.trafos.DiscreteFourierTransform(
                self.domain, axes=axes, halfcomplex=halfcomplex,
                impl=fft_impl)
            self._factor = 1.0
        else:
            self._transform = None
            self._factor = None

        if ker_mode == 'real':
            self._kernel = self.domain.element(kernel)
            self._kernel_transform = None
        else:
            self._kernel = None
            self._kernel_transform = self.transform.range.element(kernel)

        self._cache_ker_ft = bool(kwargs.pop('cache_ker_ft', False))

    @property
    def impl(self):
        """Implementation of this operator."""
        return self._impl

    @property
    def kernel_mode(self):
        """The way in which the kernel is specified."""
        return self._kernel_mode

    @property
    def transform(self):
        """Fourier transform operator back-end if used, else `None`."""
        return self._transform

    @property
    def use_transform(self):
        """Return `True` if an FT or DFT is used, otherwise `False`."""
        return self.transform is not None

    @property
    def kernel(self):
        """Real-space kernel of this transform if used, else `None`."""
        return self._kernel

    @property
    def kernel_transform(self):
        """Fourier-space kernel of this transform.

        It is either given as a parameter in the initialization or
        calculated during the first evaluation if caching was enabled.
        Otherwise, `None` is returned.
        """
        return self._kernel_transform

    def _call(self, x, out, **kwargs):
        """Implement ``self(x, out[, **kwargs])``.

        Keyword arguments are passed on to the transform.
        """
        if not self.use_transform:
            raise NotImplementedError('only transform-based convolution '
                                      'implemented.')

        if self.domain.field == odl.ComplexNumbers():
            # Use out as a temporary
            tmp = self.transform.range.element(out.asarray())
        else:
            tmp = None

        x_trafo = self.transform(x, out=tmp, **kwargs)
        if self.kernel_transform is None:
            if self.kernel is None:
                raise RuntimeError('invalid state: both kernel and '
                                   'kernel_transform are None.')

            self._kernel_transform = self.transform(self.kernel, **kwargs)

        x_trafo *= self.kernel_transform
        if self._factor != 1.0:
            x_trafo *= self._factor

        self.transform.inverse(x_trafo, out=out, **kwargs)


if __name__ == '__main__':
    # Parameters for the gaussian kernel
    gamma = 0.1
    norm_const = 2 * np.pi * gamma ** 2

    def gaussian(x):
        sum_sq = sum(xi ** 2 for xi in x)
        return np.exp(-sum_sq / (2 * gamma ** 2)) / norm_const

    # Test function
    def square(x):
        onedim_arrs = [np.where((xi >= -1) & (xi <= 1), 1.0, 0.0) for xi in x]
        out = onedim_arrs[0]
        for arr in onedim_arrs[1:]:
            out = out * arr
        return out

    space = odl.uniform_discr([-2, -2], [2, 2], (2048, 2048))

    # Showing just for fun
    real_ker = space.element(gaussian)
    real_ker.show(title='Gaussian kernel')
    func = space.element(square)
    func.show(title='Test function, a square')

    conv = Convolution(space, kernel=gaussian, kernel_mode='real',
                       impl='pyfftw_ft')

    out = space.element()
    conv.transform.create_temporaries()
    conv.transform.init_fftw_plan()

    with odl.util.testutils.Timer('first run, mode real'):
        func_conv = conv(func, out=out)

    with odl.util.testutils.Timer('second run, mode real'):
        func_conv = conv(func, out=out)

    conv.transform.create_temporaries()
    with odl.util.testutils.Timer('third run, mode real, with tmp'):
        func_conv = conv(func, out=out)

    func_conv.show(title='Convolved function')

    # Giving the kernel via FT
    ft = odl.trafos.FourierTransform(space, impl='pyfftw')
    ker_ft = ft(gaussian)
    ker_ft.show(title='FT of Gaussian kernel, half-complex')

    conv_with_ker_ft = Convolution(space, kernel=ker_ft, kernel_mode='ft_hc',
                                   impl='pyfftw_ft')

    with odl.util.testutils.Timer('first run, mode ft_hc'):
        func_conv = conv_with_ker_ft(func, out=out)

    conv_with_ker_ft.transform.create_temporaries()
    with odl.util.testutils.Timer('second run, mode ft_hc, using tmp'):
        func_conv = conv_with_ker_ft(func, out=out)

    func_conv.show(title='Convolved function, using kernel ft')
