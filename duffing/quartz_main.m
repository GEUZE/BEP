clear all
close all
clc

global w0 epsilon delta gamma alpha w
w0 = 1;
epsilon = 1;
delta = 0.4;
gamma = 5;
alpha = 0.012;

N = 1000;
x0 = [0 0];
wspan = linspace(0.001,2*w0,N);
options = optimset('display','off','TolFun',1e-9);

for i = 1:N;
    w = wspan(i);
    [A,fval,exitflag] = fsolve(@quartz,x0,options); % Call solver
    if exitflag ~= 1;
        break
    end
    f_up(i) = w;
    up(i,:) = A;
    x0 = up(i,:);
    jump_down = i;
end

% jump_down = 2000;

if jump_down ~= 2000

    
    x0(1) = 0.975 * x0(1);
    x0(2) = 1/0.975 * x0(2);
    
    for i = 1:jump_down-1;
        w = wspan(jump_down - i);
        [A,fval,exitflag] = fsolve(@quartz,x0,options); % Call solver
        if exitflag ~= 1;
            break
        end
        f_unstable(i) = w;
        unstable(i,:) = A;
        x0 = unstable(i,:);
        jump_up = i;
    end

    x0(1) = 0.975 * x0(1);
    x0(2) = 1/0.975 * x0(2);
    
    for i = 1:(N - jump_down + jump_up)
        w = wspan(jump_down - jump_up + i);
        [A,fval,exitflag] = fsolve(@quartz,x0,options); % Call solver
        if exitflag ~= 1;
            break
        end
        f_down(i) = w;
        down(i,:) = A;
        x0 = 0.99 * down(i,:);
    end

    plot(horzcat(f_up,f_unstable,f_down),vertcat(abs(up(:,1)),abs(unstable(:,1)),abs(down(:,1))))
    figure(2)
    plot(horzcat(f_up,f_unstable,f_down),vertcat(abs(up(:,2)),abs(unstable(:,2)),abs(down(:,2))))
else
    plot(f_up,up(:,1))
    figure(2)
    plot(f_up,up(:,2))
end