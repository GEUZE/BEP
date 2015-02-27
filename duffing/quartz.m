function F = quartz(x) % r = y(1), phi = y(2)
global w0 epsilon delta gamma alpha w
F = [(epsilon/(2*w)) * (-w*delta*x(1) - gamma*sin(x(2)));
     (epsilon/(2*w)) * (-(w^2 - w0^2)*x(1) + (3/4)*alpha*x(1)^3 - gamma*cos(x(2)))];
 
