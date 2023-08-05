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

"""Example showing how to use vectorization of FunctionSpaceVector's."""

# Imports for common Python 2/3 codebase
from __future__ import print_function, division, absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import super

import numpy as np
import odl


_SUPPORTED_IMPL = ('numpy_ft', 'numpy_dft', 'pyfftw_ft', 'pyfftw_dft')
_SUPPORTED_KER_MODES = ('real', 'ft', 'dft', 'ft_hc', 'dft_hc')


class Convolution(odl.Operator):

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
    def axes(self):
        """Axes along which the convolution is taken."""
        if not self.use_transform:
            # TODO: store if no transform used
            return None
        else:
            return self.transform.axes

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
            self._kernel_transform = self._ker_trafo()

        x_trafo *= self.kernel_transform
        if self._factor != 1.0:
            x_trafo *= self._factor

        self.transform.inverse(x_trafo, out=out, **kwargs)

    def _ker_trafo(self, **kwargs):
        """Helper for the calculation of the kernel transform."""
        if self.kernel is None:
            raise RuntimeError('invalid state: both kernel and '
                               'kernel_transform are None.')

        return self.transform(self.kernel, **kwargs)

    @property
    def adjoint(self):
        """Adjoint operator."""
        if self.kernel_transform is None:
            self._kernel_transform = self._ker_trafo()

        # TODO: add conj to DiscreteLpVector
        adj_kernel_ft = self.transform.range.element(
            self.kernel_transform.asarray().conj())

        if self.transform.halfcomplex:
            kernel_mode = 'ft_hc'
        else:
            kernel_mode = 'ft'
        return Convolution(dom=self.domain,
                           kernel=adj_kernel_ft, kernel_mode=kernel_mode,
                           impl=self.impl, axes=self.axes)

# ---- Example 1 -----


def step(x):
    return np.where(x <= 0, 1 + x, 2 - 2 * x)


def var_exponent(x):
    return np.where(np.abs(x) <= 0.2, 1, 2)


discr = odl.uniform_discr(-1, 1, 100, exponent=2)
step_discr = discr.element(step)
# fig = step_discr.show()

var_exp_discr = discr.element(var_exponent)
# var_exp_discr.show(fig=fig)

var_lp_functional = VariableLpFunctional(discr, var_exponent)
# print('Variable Lp functional value: ', var_lp_functional(step))
# print('Variable Lp, constant 1:', var_lp_functional(discr.one()))


# ---- End Example 1 ----


class VariableLpFunctional(odl.Operator):

    """Functional for evaluating the variable Lp "norm".

    The variable Lp functional is defined as::

        S(f) = integral_Omega ( |f(x)|^(p(x)) / p(x) dx )

    It maps a space X of real-valued functions on Omega to the
    real numbers. The exponent function is expected to .
    """

    def __init__(self, space, var_exp):
        """Initialize a new instance.

        Parameters
        ----------
        space : `DiscreteLp` or `ProductSpace`
            The latter is interpreted as a product of discrete
            function spaces.
        var_exp : scalar-valued ``space`` `element-like`
            The variable exponent ``p(x)``
        """
        super().__init__(space, space.field, linear=False)
        if isinstance(self.domain, odl.ProductSpace):
            self.var_exp = self.domain[0].element(var_exp)
        else:
            self.var_exp = self.domain.element(var_exp)

    def _call(self, x):
        """Evaluate the functional in ``x``."""
        if isinstance(self.domain, odl.ProductSpace):
            return self._call_pspace(x)
        else:
            return self._call_scalar(x)

    def _call_scalar(self, x):
        """"""
        tmp = np.power(np.abs(x), self.var_exp / self.domain.exponent)
        tmp /= self.var_exp.asarray() ** (1 / self.domain.exponent)
        return self.domain.norm(tmp) ** self.domain.exponent

    def _call_pspace(self, x):
        # TODO: this may need to be adapted for product spaces

        # We calculate (||y||_q)^q, where q is the exponent of this
        # space, and y = (|f(x)|^(p(x)) / p(x))^(1/q)
        # The first few lines are for the pointwise calculation of the norm
        # of the vector-valued function x
        y = x.ufunc.absolute()
        tmp = x[0].space.element()
        sq_tmp = x[0].space.element()
        for x_i in y[1:]:
            sq_tmp.multiply(x_i, x_i)
            tmp += sq_tmp
        tmp.ufunc.sqrt(out=tmp)

        tmp **= self.var_exp / self.domain.exponent
        tmp /= self.var_exp.asarray() ** (1 / self.domain.exponent)
        return tmp.norm() ** self.domain.exponent

    def derivative(self, x):
        """Return the Frechet derivative at ``x``."""
        grad = VariableLpGradient(self.domain, self.var_exp)
        return grad(x).T


class VariableLpGradient(odl.Operator):

    """Operator for evaluation of the variable Lp derivative.

    The formal gradient of the variable Lp functional is given by::

        grad S(F)(x) = |F(x)|^(p(x) - 2) * F(x)

    """

    def __init__(self, space, var_exp):
        """Initialize a new instance.

        Parameters
        ----------
        space : `DiscreteLp` or `ProductSpace`
            The latter is interpreted as a product of discrete
            function spaces.
        var_exp : ``space`` `element-like`
            The variable exponent ``p(x)``
        """
        # TODO: adapt for product spaces
        super().__init__(space, space, linear=False)
        self.var_exp = self.domain.element(var_exp)

    def _call(self, x):
        """Evaluate the functional in ``x``."""
        if isinstance(self.domain, odl.ProductSpace):
            return self._call_pspace(x)
        else:
            return self._call_scalar(x)

    def _call_pspace(self, x):
        """Evaluate the gradient in ``x``."""
        y = x.ufunc.absolute()
        tmp = x[0].space.element()
        sq_tmp = x[0].space.element()
        for x_i in y[1:]:
            sq_tmp.multiply(x_i, x_i)
            tmp += sq_tmp

        tmp **= self.var_exp / 2 - 1
        mul_op = odl.MultiplyOperator(tmp)
        bc_op = odl.BroadcastOperator([mul_op] * self.domain.size)
        return bc_op(x)

    def _call_scalar(self, x):
        """Scalar version."""
        tmp = np.power(np.abs(x), self.var_exp - 2)
        return tmp * x


class VariableLpTVGradient(VariableLpGradient):

    """Operator for evaluation of the variable Lp TV gradient.

    The formal gradient of the variable Lp functional is given by::

        grad S(F)(x) = -div( |grad(f)(x)|^(p(x) - 2) * grad(f)(x) )

    """

    def _call_pspace(self, x):
        if isinstance(self.domain, odl.ProductSpace):
            raise NotImplementedError
        grad_op = odl.Gradient(self.domain)



# ---- Example 2 ----


def step(x):
    return np.where(x <= 0, 1 + x, 2 - 2 * x)


def var_exponent(x):
    return np.where(np.abs(x) <= 0.2, 1, 2)


#discr = odl.uniform_discr(-1, 1, 100, exponent=2)
#step_discr = discr.element(step)
#step_discr.show(title='Step function')
#
#var_exp_discr = discr.element(var_exponent)
#var_exp_discr.show(title='Exponent function')
#
#var_lp_functional = VariableLpFunctional(discr, var_exponent)
#var_lp_gradient = VariableLpGradient(discr, var_exponent)
#
#
#grad_at_step = var_lp_gradient(step)
#grad_at_step.show(title='Gradient at the step function')
#
#deriv_at_step = var_lp_functional.derivative(step)
#print('Variable Lp derivative at step, applied to one: ',
#      deriv_at_step(discr.one()))


# ---- End example 2 ----

# ---- Example 3 ----

sigma = 0.05


def gaussian(x):
    return np.exp(-x**2 / (2 * sigma ** 2))

discr = odl.uniform_discr(-1, 1, 1000, exponent=2)
step_discr = discr.element(step)
step_discr.show(title='Step function')

kernel = discr.element(gaussian)
kernel.show(title='Convolution kernel')

conv = Convolution(dom=discr, kernel=gaussian)
data = conv(step)
data.show(title='Data - convolved step function')

#tmp = conv.adjoint(step)
#tmp.show(title='Adjoint')


# ---- TV reconstruction

#gradient = odl.Gradient(discr, method='forward')
#op = odl.ProductSpaceOperator([[conv],
#                               [gradient]])
#
## Choose a starting point
#x = op.domain.one()
#
## Estimated operator norm, add 10 percent to ensure ||K||_2^2 * sigma * tau < 1
#op_norm = 1.1 * odl.operator.oputils.power_method_opnorm(op, 100)
#print('Norm of the product space operator: {}'.format(op_norm))
#
## Create the proximal operator for unconstrained primal variable
#proximal_primal = odl.solvers.proximal_zero(op.domain)
#
## Create proximal operators for the dual variable
#
## l2-data matching
#prox_convconj_l2 = odl.solvers.proximal_convexconjugate_l2(discr, g=data)
#
## TV-regularization i.e. the l1-norm
#prox_convconj_l1 = odl.solvers.proximal_convexconjugate_l1(
#    gradient.range, lam=0.01)
#
## Combine proximal operators, order must correspond to the operator K
#proximal_dual = odl.solvers.combine_proximals(
#    [prox_convconj_l2, prox_convconj_l1])
#
## Number of iterations
#niter = 20000
#
## Step size for the proximal operator for the primal variable x
#tau = 1 / op_norm
#
## Step size for the proximal operator for the dual variable y
#sigma = 1 / op_norm
#
## Optionally pass partial to the solver to display intermediate results
#partial = (odl.solvers.util.PrintIterationPartial() &
#           odl.solvers.util.PrintTimingPartial() &
#           odl.solvers.util.ShowPartial(display_step=1000))
#
## Run the algorithm
#odl.solvers.chambolle_pock_solver(
#    op, x, tau=tau, sigma=sigma, proximal_primal=proximal_primal,
#    proximal_dual=proximal_dual, niter=niter, partial=partial)


# --- Variable Lp reconstruction with gradient method ---

#op_norm = 1.1 * odl.operator.oputils.power_method_opnorm(var_lp_functional,
#                                                         100)
#test = odl.diagnostics.OperatorTest(var_lp_functional)
#test.run_tests()


def var_exponent_const(x):
    return 1.01 * np.ones_like(x)


reg_param = 0.00001

var_lp_functional = VariableLpFunctional(discr, var_exponent_const)
var_lp_gradient = VariableLpGradient(discr, var_exponent_const)


# Define line search method for the BFGS optimizer
linesearch = odl.solvers.BacktrackingLineSearch(var_lp_functional)
fstart = discr.one()
l2_grad = conv.adjoint * odl.operator.ResidualOperator(conv, data)
obj_grad = l2_grad + reg_param * var_lp_gradient

partial = odl.solvers.ShowPartial(display_step=100)
odl.solvers.steepest_descent(obj_grad, fstart, niter=2000, line_search=0.5,
                             partial=partial)
