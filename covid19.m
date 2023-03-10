function covid19(~)
% Epidemic simulation.
% See: https://blogs.mathworks.com/cleve/2020/03/29/second-version-of-a-covid-19-simulator/
%
% There are six types of individuals.
%
%   Young      Bright blue. Individuals created during the simulation.
%
%   Adult      Blue. Susceptible, on the move.
%
%   Mature     Dark blue-green. Susceptible, stay at home.
%              
%   Sick       Red. Infected. Infects others when they too close.
%             
%   Immune     Red circle. Previously infected. No longer virulent.
%              
%   Dead       Infected individuals deleted from simulation.  Just counted.
%
% There are eight controllable parameters.
%
%   n           Population size.
%   infect      Time steps between introduction of new sick adults.
%   birth       Birth rate.
%   mortality   Mortality rate.
%   virulence   Radius of effectiveness of sick individuals.
%   duration    Time steps before a sick individual becomes immune.
%   speed       Time steps between display updates.
%   barrier     Length of barrier separating two halves of the region.
%
% The epidemic begins with infected individuals entering from the northeast corner.
% The epidemic ends when there are no more infected individuals.
%
% Inspired by a Washington Post graphic by Harry Stevens, March 14, 2020.
% https://www.washingtonpost.com/graphics/2020/world/corona-simulator/?itid=sf_\

%   Copyright 2020 Cleve Moler
%   Copyright 2020 The MathWorks, Inc.

    % Parameters in the control panel.
    
    n = 100;           % initial population size
    infect = 10;       % interval between new sick individuals
    birth = .020;      % birth rate
    mortality = .050;  % mortality rate
    virulence = .020;  % infectious distance
    duration = 50;     % time of infection
    speed = 1;         % interval between display updates
    barrier = .70;     % barrier length
    
    randu = @(n,m) 2*rand(n,m)-1;  % Uniform random in [-1 1]
    
    % Fixed parameters
        
    bw = .02;          % barrier width
    ms = 24;           % markersize 
    epidemic = 5;      % durations per epidemic
    stepsize = .03;
    tmax = 2000;
    fontsize = 10;
    fontname = get(groot,'fixedwidthfontname');  % fixed width

    % ---------------------------------------------------------
       
    A = [];
    data = [];
    deaths = []; 
    figs = gcf;
    n0 = n;
   
    if nargin == 1
        thumbnail 
        return
    end
    
    [paws,stop,census] = init_gui;
    
    restart_callback
          
    while get(stop,'value') == 0
        
        % Census
        count = histc(A.type,1:5);
        count(6) = deaths;
        % Update display 
        if mod(t,speed) == 0
            for k = 1:n
               set(A.p(k),'xdata',A.x(k),'ydata',A.y(k))
            end
            xlabel(t)
            title(n)
            set(census,'string',num2str(count,'%3d'))
            drawnow limitrate
        end
        
        % Skip rest of loop if no more sick or pause or runaway simulation
        if (t > 0 && count(4) == 0) || get(paws,'value') == 1 || t >= tmax
            continue
        end
     
        if t > 0
            data(:,end+1) = count;
        end
            
        % Introduce new virus
        if t <= epidemic*duration && mod(t,infect) == 0
            introduce_sick
        end

        % Time step
        A.x = A.x + stepsize*A.u;
        A.y = A.y + stepsize*A.v;
        A.age = A.age + 1/10;
        t = t + 1;
        
        % Bounce off sides
        k = find(abs(A.x) > 1-stepsize);
            A.x(k) = sign(A.x(k))*(1-stepsize);
            A.u(k) = -A.u(k);
        k = find(abs(A.y) > 1-stepsize);
            A.y(k) = sign(A.y(k))*(1-stepsize);
            A.v(k) = -A.v(k);

        % Bounce off barrier
        k = find(abs(A.y) >= (1-barrier) & abs(A.x) < 2*bw);
            A.x(k) = 2*bw*sign(A.x(k));
            A.u(k) = -A.u(k);

        % Possibly infectious encounters
        z = A.x + A.y*1i;
        d = triu(abs(z - z.'));
        [r,q] = find(0 < d & d < virulence);
        for k = 1:length(r)
            rk = A.type(r(k));
            qk = A.type(q(k));
            if rk == 4 && qk <= 3
                A.type(q(k)) = 4;
                set(A.p(q(k)),'color',colors(4));
                A.t(q(k)) = t;
            end
            if qk == 4 && rk <= 3
                A.type(r(k)) = 4;
                set(A.p(r(k)),'color',colors(4));
                A.t(r(k)) = t;
            end
        end
        
        % births
        if rand < birth*n/100
            narg = findobj('tag','n+');
            n_callback(narg);
            A.age(n) = 0;
        end
                 
        % deaths
        nv = count(4)+count(5);
        if rand < mortality*nv/10
            narg = findobj('tag','n-');
            n_callback(narg,nv)
        end
        
        % young -> adult at 20
        f = (A.type == 1) & (A.age >= 20);
        A.type(f) = 2;  
        set(A.p(f),'color',colors(2))

        % adult -> mature at 60
        f = (A.type == 2) & (A.age >= 60);
        A.type(f) = 3;
        set(A.p(f),'color',colors(3))
        A.u(f) = 0;
        A.v(f) = 0;
        
        % sick -> immune after duration time steps
        f = (A.type == 4) & (A.t < t - duration);
        A.type(f) = 5; 
        set(A.p(f),'marker','o', ...
            'markersize',ms/4, ...
            'linewidth',1, ...
            'color',colors(5));
    end
    close(figs)

    % ----------------------------------------------------------------------
    
    function restart_callback(~,~)
        axis([-1 1 -1 1])
        axis square
        noticks
        t = 0;
        n0 = n;
        shg
        
        drawnow limitrate
        cla
        make_barrier(barrier,bw)
        t = 0;                       % time
        deaths = 0;
        data = zeros(6,0);
        narg = findobj('tag','n+');
        A.x = randu(n,1);            % initial position, [-1,1]
        A.y = randu(n,1);
        A.u = randu(n,1);            % constant velocity, [-1,1]
        A.v = randu(n,1);
        A.type = 2*ones(n,1);        % adults
        A.age = 20 + 22*randn(n,1);  % 20 < age < 42
        A.t = zeros(n,1);            % time stamp
        A.p = zeros(n,1);            % graphics pointer
        c = colors(2);
        for k = 1:n
            A.p(k) = line(A.x(k),A.y(k), ...
                'linestyle','none', ...
                'marker','.', ...
                'color',c, ...
                'markersize',ms);
        end
    end

    function [paws,stop,census] = init_gui
        if isequal(get(gcf,'name'),'covid19-1')
            clf
        else
            set(gcf,'name','covid19-1','numbertitle','off')
        end
        uicontrol('style','pushbutton', ...
            'units','normal', ...
            'position',[.86 .87 .10 .05], ...
            'background','w', ...
            'string','restart', ...
            'fontsize',fontsize, ...
            'fontweight','bold', ...
            'callback',@restart_callback);
        paws = uicontrol('style','toggle', ...
            'units','normal', ...
            'position',[.86 .52 .10 .05], ...
            'background','w', ...
            'string','pause', ...
            'fontweight','bold', ...
            'fontsize',fontsize);
        stop = uicontrol('style','toggle', ...
            'units','norm', ...
            'position',[.86 .80 .10 .05], ...
            'string','close', ...
            'background','w', ...
            'fontweight','bold', ...
            'fontsize',fontsize);
        help_callback = @(~,~) doc('covid19');
        uicontrol('style','push', ...
            'units','norm', ...
            'position',[.86 .73 .10 .05], ...
            'string','help', ...
            'background','w', ...
            'fontsize',fontsize, ...
            'fontweight','bold', ...
            'callback',help_callback);
        blog_callback = @(~,~) ...
            web('https://blogs.mathworks.com/cleve/2020/03/29/second-version-of-a-covid-19-simulator');
        uicontrol('style','push', ...
            'units','norm', ...
            'position',[.86 .66 .10 .05], ...
            'string','blog', ...
            'background','w', ...
            'fontsize',fontsize, ...
            'fontweight','bold', ...
            'callback',blog_callback);
        uicontrol('style','push', ...
            'units','norm', ...
            'position',[.86 .59 .10 .05], ...
            'string','plot', ...
            'background','w', ...
            'fontsize',fontsize, ...
            'fontweight','bold', ...
            'callback',@plot_callback);
    
        types = 'young  adult  mature sick   immune deaths ';
        uicontrol('style','frame', ...
            'units','normal', ...
            'position',[.835 .20 .155 .25], ...
            'background','w')
        uicontrol('style','text', ...
            'units','normal', ...
            'position',[.84 .22 .09 .21], ...
            'fontname',fontname, ...
            'fontsize',fontsize, ...
            'fontweight','bold', ...
            'background','w', ...
            'horiz','left', ...
            'string',types)
        census = uicontrol('style','text', ...
            'units','normal', ...
            'position',[.938 .22 .05 .21], ...
            'fontname',fontname, ...
            'fontsize',fontsize, ...
            'fontweight','bold', ...
            'background','w', ...
            'horiz','right', ...
            'string',num2str(zeros(6,1),'%3d'));
        parm(n,'n: %d',@n_callback,1);
        parm(infect,'infect: %d',@infect_callback,2);
        parm(birth,'birth: %5.3f',@birth_callback,3);
        parm(mortality,'mortality: %5.3f',@mortality_callback,4);
        parm(virulence,'virulence: %5.3f',@virulence_callback,5);
        parm(duration,'duration: %d',@duration_callback,6);
        parm(speed,'speed: %d',@speed_callback,7);
        parm(barrier,'barrier: %5.3f',@barrier_callback,8);
    end

    function label = parm(val,fmt,callback,pos)
        label = uicontrol('style','text', ...
            'units','normalized', ...
            'position',[.015 1.0-.11*pos .187 .05], ...
            'fontsize',fontsize, ...
            'fontweight','bold', ...
            'horiz','left', ...
            'userdata',fmt, ...
            'string',sprintf(fmt,val));
        name = fmt(1:find(fmt==':')-1);
        pm = '+-';
        for j = 1:2
            uicontrol('string',pm(j), ...
                'fontsize',fontsize, ...
                'units','normalized', ...
                'fontweight','bold', ...
                'position',[.13-.05*j 0.96-.11*pos .04 .04], ...
                'background','white', ...
                'userdata',label, ...
                'tag',[name pm(j)], ...
                'callback',callback);
        end
    end

    function display_parm_value(arg,val)
        label = get(arg,'userdata');
        fmt = get(label,'userdata');
        set(label,'string',sprintf(fmt,val))
    end

    function introduce_sick
        n = n + 1;
        narg = findobj('tag','n+');    
        display_parm_value(narg,n)
        A.type(n) = 4;   % sick
        A.x(n) = 1;      % upper right corner
        A.y(n) = 1;
        A.u(n) = -rand;
        A.v(n) = -rand;
        A.age(n) = inf;
        A.t(n) = t;
        A.p(n) = line(A.x(n),A.y(n), ...
            'linestyle','none', ...
            'marker','.', ...
            'color',colors(4), ...
            'markersize',ms);
    end
  
    function n_callback(arg,~)
        % Callback for decreasing or increasing n.
        if get(arg,'string') == '-'
            if n == 1
                return
            end
            if nargin > 1   % Limit to sick or immune
                j = find(A.type > 3);
                if isempty(j)
                    return
                end
                k = j(ceil(rand*length(j)));
            else
                k = 1 + floor(rand*n);
            end
            delete(A.p(k))
            A.type(k) = [];
            A.x(k) = [];
            A.y(k) = [];
            A.u(k) = [];
            A.v(k) = [];
            A.t(k) = [];
            A.p(k) = [];
            A.age(k) = [];
            n = n - 1;
            deaths = deaths + 1;
        else % '+'
            n = n + 1;
            A.type(n) = 1;   % young
            A.x(n) = randu(1,1);
            A.y(n) = randu(1,1);
            A.u(n) = randu(1,1);
            A.v(n) = randu(1,1);
            A.age(n) = 0;
            A.t(n) = t;
            A.p(n) = line(A.x(n),A.y(n), ...
                'linestyle','none', ...
                'marker','.', ...
                'color',colors(1), ...
                'markersize',ms);
        end
        display_parm_value(arg,n)
    end

    function v = plus_or_minus(v,d,pm)
        if get(pm,'string') == '+'
            if v < .999*d
                v = v + d/10;
            elseif v < 10*d
                v = v + d;
            else
                v = v + 10*d;                                
            end
        elseif v > 0
            if v > 10*d
                v = v - 10*d;
            elseif v > d
                v = v - d;
            elseif d ~= 1 
                v = max(0,v - d/10);
            end
        else
            % v = v;
        end       
        display_parm_value(pm,v)
    end

    function infect_callback(pm,~)
        % Time steps between introduction of new sick adults.
        infect = plus_or_minus(infect,10,pm);
    end

    function birth_callback(pm,~)
        % Birth rate.
        birth = plus_or_minus(birth,.01,pm);
    end

    function mortality_callback(pm,~)
        % Death rate.
        mortality = plus_or_minus(mortality,.01,pm);
    end

    function virulence_callback(pm,~)
        % Effective radius of infection).
        virulence = plus_or_minus(virulence,.01,pm);
    end

    function duration_callback(pm,~)
        % Time steps to become immune.
       duration = plus_or_minus(duration,10,pm);
    end

    function speed_callback(pm,~)
        % Time interval between frames
        speed = plus_or_minus(speed,1,pm);
    end

    function barrier_callback(pm,~)
        % Length of central barrier.
        if get(pm,'string') == '-'
            if round(100*barrier) <= 90
                barrier = barrier - .10;
            else
                barrier = barrier - .01;
            end
        else
            if barrier >= 1
                % do nothing
            elseif round(100*barrier) >= 90
                barrier = barrier + .01;
            else
                barrier = barrier + .10;
            end
        end
        display_parm_value(pm,barrier)
        make_barrier(barrier,bw)
    end

    function make_barrier(barrier,bw)
        % Resize barrier
        bx = [bw bw -bw -bw];
        by = [1 1-barrier 1-barrier 1];
        grey = [.9 .9 .9];
        delete(findobj('type','patch'))
        patch(bx,by,grey)
        patch(bx,-by,grey)
    end

    function color = colors(n)
    % [light-blue blue blue-green red red black]   
        blue = 1.1*[.00 .45 .75];
        red = [.63 .08 .18];
        black = [0 0 0];
        clrs = [blue.*[0 0 1]
                blue.*[0 .75 .75]
                blue.*[0 1 0]
                red
                red
                black];
        if nargin == 1
            color = clrs(n,:);
        else
            color = clrs;
        end
    end

    function noticks
        % noticks
        set(gca,'xtick',[],'ytick',[])
        box on
    end

    function thumbnail
        % Thumbnail for Cleve_Lab 
        n = 5+ceil(rand*(n-20));
        ms = 16;
        barrier = rand;
        restart_callback(true)
        set(A.p(1:ceil(n/3)),'color',colors(4))
    end

    function plot_callback(~,~)
        fig1 = gcf;
        pos1 = get(gcf,'pos');        
        fig2 = figure('units',get(fig1,'units'));
        figs(end+1) = fig2;
        pos1(1) = 0.1*pos1(3);
        pos2 = pos1;
        pos2(1) = pos1(1)+1.1*pos1(3);
        set(fig1,'pos',pos1)
        set(fig2,'pos',pos2)
        set(fig2,'numbertitle','off', ...
            'name',['covid19-' num2str(length(figs))]);
        figure(fig2)

        plot(data','linewidth',2)
        set(gca,'xlim',[1 size(data,2)],'fontsize',fontsize)
        legend({'young ','adult ','mature','sick  ','immune','deaths'}, ...
           'location','best')
        title(sprintf( ...
            ['    n0   infect   birth mortality virulence duration barrier\n' ...
            '%d  %7d  %7.3f  %8.3f  %9.3f  %8d  %8.3f'], ...
            n0,infect,birth,mortality,virulence,duration,barrier))
        figure(fig1)
    end
end
        