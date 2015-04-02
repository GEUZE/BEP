close all
clear all
clc

global mass w0 epsilon delta gamma alpha w
mass = 1;
w0 = sqrt(0.75)*1;
epsilon = 0.75;
delta = 0.2;
gamma = 2.5;
alpha = 0.03;

G=11;
gamma_span = linspace(1,4,G);
N = 1000;
Color = {'k','b','r','g','y','k','b','r','g','y','k','b','r','g','y','k','b','r','g','y'};


wspan = linspace(0.001,2*w0,N);
options = optimset('MaxFunEvals',500,'display','off','TolFun',1e-9);

       
for k = 1:G;
    clear f_up up f_unstable unstable f_down down
    gamma = gamma_span(k);
    x0 = [gamma 0];
    
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
        jump_down_w(k) = wspan(jump_down);
    end
    
    % jump_down = 2000;
    
    if jump_down ~= 99999
        
        
        x0(1) = 0.975 * x0(1);
        x0(2) = (1/0.975) * x0(2);
        
        for i = 1:jump_down-1;
            w = wspan(jump_down - i);
            [A,fval,exitflag] = fsolve(@quartz,x0,options); % Call solver
            if exitflag ~= 1;
                break
            end
            f_unstable(i) = w;
            unstable(i,:) = A;
            x0(1) = 0.975*unstable(i,1);
            x0(2) = (1/0.975)*unstable(i,2);
            jump_up = i;
            jump_up_w(k) = wspan(jump_down-jump_up);
        end
        
        x0(1) = 0.94 * x0(1);
        x0(2) = (1/0.98) * x0(2);
        
        for i = 1:(N - jump_down + jump_up)
            w = wspan(jump_down - jump_up + i);
            [A,fval,exitflag] = fsolve(@quartz,x0,options); % Call solver
            if exitflag ~= 1;
                break
            end
            f_down(i) = w;
            down(i,:) = A;
            x0(1) = 0.975 * down(i,1);
            x0(2) = (1/0.975) * down(i,2);
        end
        
        frequency_up{k} = f_up;
        frequency_unstable{k} = f_unstable;
        frequency_down{k} = f_down;
        
        amplitude_up{k} = up(:,1);
        amplitude_unstable{k} = unstable(:,1);
        amplitude_down{k} = down(:,1);
        
        phase_up{k} = up(:,2);
        phase_unstable{k} = unstable(:,2);
        phase_down{k} = down(:,2);
        
        frequency{k} = horzcat(f_up,f_unstable,f_down);
        amplitude{k} = vertcat(abs(up(:,1)),abs(unstable(:,1)),abs(down(:,1)));
        phase{k} = pi - vertcat(abs(up(:,2)),abs(unstable(:,2)),abs(down(:,2)));
        
    else
        frequency_up{k} = f_up;
        amplitude_up{k} = up(:,1);
        phase_up{k} = up(:,2);
        
        frequency{k} = f_up;
        amplitude{k} = up(:,1);
        phase{k} = up(:,2);
        
    end
    legenda{k} = horzcat('\gamma = ',num2str(gamma));
    figure(1)
    hold on
    plot(frequency{k},amplitude{k},Color{k})
    hold off
    figure(2)
    hold on
    plot(frequency{k},phase{k},Color{k}),
    hold off
end
figure(1)
xlabel('\omega/\omega_0')
ylabel('r')
legend(legenda)
figure(2)
xlabel('\omega/\omega_0')
ylabel('\phi')
axis([0 2 0 pi])
ax = gca;
set(ax,'YTick',[0,pi/2,pi]);
set(ax,'YTickLabel',{'-pi','-pi/2',0});
legend(legenda)
figure(3)
xlabel('\omega/\omega_0')
ylabel('\gamma')
plot(jump_down_w,gamma_span,jump_up_w,gamma_span)