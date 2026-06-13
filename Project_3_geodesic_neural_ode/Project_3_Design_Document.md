# Project 3 Design Document
## Neural ODE Learning Geodesic Flow on the Poincaré Disk

---

## 1. Mathematical Setup
- Model: Poincaré disk — A Euclidean unit disk with hyperbolic metric in the following
- Metric: ds^2 = 4 (dx^2 + dy^2) /(1 - x^2 - y^2)^2
- Geodesics: the counterpart on surfaces of line segments of plane, on Poincaré disk, in particular, they are circular arcs orthogonal to the boundary circle or diameters
- State space: the unit tangent bundle of the surface, which is 3-dimensional (the space of baseponits is 2-dimensional, and the space of all unit tangent vectors is 1-dimensional)

## 2. Data Generation
- N = 1000 training pairs
- Each pair: (x0, x_target) where x0 is the initial unit tangent vector and the x_target is the tangent vector at time T = 1.0 with information of their respective basempoints
- Sampling: positions sampled uniformly within radius 0.8 with angle \theta sampled uniformly in [0 , 2\pi)
- Ground truth: we will use the geodesic equation to analytically compute x_target for each x0

## 3. Network Architecture
- Input: x of shape (3,)
- Layers: nn.Linear(3, 64) , nn.Tanh(), nn.Linear(64 , 64), nn.Tanh(), nn.Linear(64 , 3)
- Output: dx/dt of shape (3,), instantaneous velocity on the unit tangent bundle
- Tanh: make sure the smoothness of the learned trajectory

## 4. Training Setup
- Optimizer: torch.optim.Adam(func.parameters(), lr = 1e-3)
- Loss: Criterion = nn.MSELoss()
- Epochs: epochs = 1000
- Solver: odeint(func, x0, t, method = 'dopri5')
- Train/val split: 80% train, 20% validation, split before training

## 5. Evaluation
- Metric: measure the mean square of (x_pred - x_target)^2 
- Visualization: plot both the analytic geodesic and the learned trajectory on the Poincaré disk for several test pairs, overlaid on the same figure