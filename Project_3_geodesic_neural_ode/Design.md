# Project 3 Design Document
## Neural ODE Learning Geodesic Flow on the Poincaré Disk

---

## 1. Mathematical Setup
- Model: Poincaré disk — A Euclidean unit disk with hyperbolic metric in the following
- Metric: ds^2 = 4 (dx^2 + dy^2) /(1 - x^2 - y^2)^2
- Geodesics: the counterpart on surfaces of line segments of plane, on Poincaré disk, in particular, they are circular arcs orthogonal to the boundary circle or diameters
- State space: the unit tangent bundle of the surface, which is 3-dimensional (the space of basepoints is 2-dimensional, and the space of all unit tangent vectors is 1-dimensional)

## 2. Geodesic Equations
- Metric tensor: $$g_{ij} = \frac{4}{(1-r^2)^2} \begin{pmatrix}1&0\\ 0&1 \end{pmatrix}$$
- Christoffel symbols:
$$
\begin{aligned}
\Gamma^1_{11}&=\frac{2x}{1-r^2},\\
\Gamma^1_{12}&=\Gamma^1_{21}=\frac{2y}{1-r^2},\\
\Gamma^1_{22}&=-\frac{2x}{1-r^2},\\
\Gamma^2_{11}&=-\frac{2y}{1-r^2},\\
\Gamma^2_{12}&=\Gamma^2_{21}=\frac{2x}{1-r^2},\\
\Gamma^2_{22}&=\frac{2y}{1-r^2}.
\end{aligned}$$

- equation of the geodesic (x(t),y(t)):
 $$ \ddot x +\frac{2x}{1-r^2}(\dot x^2-\dot y^2)+\frac{4y}{1-r^2}\dot x\dot y=0$$
 $$ \ddot y +\frac{2y}{1-r^2}(\dot y^2-\dot x^2)+\frac{4x}{1-r^2}\dot x\dot y=0.$$

- First-order ODE on T^1M (x(t),y(t),\theta(t)): 
$$
\begin{aligned}
\dot x &= \frac{1-x^2-y^2}{2}\cos\theta,\\
\dot y &= \frac{1-x^2-y^2}{2}\sin\theta,\\
\dot\theta &= y\cos\theta-x\sin\theta.
\end{aligned}
$$

## 3. Data Generation
- N = 1000 training pairs
- Each pair: (state_0, state_target) where state_0=(x0, y0, θ0) is the initial unit tangent vector and the state_target=(x(T), y(T), θ(T)) is the tangent vector at time T = 1.0 obtained by integrating the geodesic flow from state_0
- Sampling: (x0, y0) sampled uniformly within radius 0.8 of the origin with θ0 sampled uniformly in $$[0, 2\pi)$$
- Ground truth: integrate the first-order ODE system from Section 2 using scipy.integrate.solve_ivp to obtain state_target

## 4. Network Architecture
- Input: x of shape (3,)
- Layers: nn.Linear(3, 64) , nn.Tanh(), nn.Linear(64 , 64), nn.Tanh(), nn.Linear(64 , 3)
- Output: dx/dt of shape (3,), instantaneous velocity on the unit tangent bundle
- Tanh: make sure the smoothness of the learned trajectory

## 5. Training Setup
- Optimizer: torch.optim.Adam(func.parameters(), lr = 1e-3)
- Loss: Criterion = nn.MSELoss()
- Epochs: epochs = 1000
- Solver: odeint(func, x0, t, method = 'dopri5')
- Train/val split: 80% train, 20% validation, split before training

## 6. Evaluation
- Metric: measure the mean square of (x_pred - x_target)^2 
- Visualization: plot both the analytic geodesic and the learned trajectory on the Poincaré disk for several test pairs, overlaid on the same figure