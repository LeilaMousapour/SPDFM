clear;
clc;

Au_20nm_Mesh

%  BEM options
op = bemoptions( 'sim', 'stat', 'interp', 'curve' );
%op = green.options('cutoff',cutoff);
%  plane wave excitation
pol= [0,1, 0]; %0, 1, 0]
dir = [1, 0, 0];% 0, 0, 1]
exc = planewave( pol, dir, op );

%  set up BEM solver
bem = bemsolver( p, op );
%bem.F
enei = linspace(400,500,1);

%Maxx_np=zeros(2,15);


for E= 1 : length(enei)
    
    sig = bem \ exc( p, enei(E) );
   

    [ x, y ] = meshgrid( linspace( -40 , 40, 100 ));

    %  set up MESHFIELD object
    emesh = meshfield( p, x, y, 0 , op, 'mindist', 0.1);
    
    %  compute field map
    e = emesh( sig ) + emesh( exc.field( emesh.pt, sig.enei ) );
    e2 = emesh( sig );
    e3 = emesh( exc.field( emesh.pt, sig.enei ) );
  
    ee=sqrt(dot( e, e, 3 ));
    ee2=sqrt(dot( e2, e2, 3 ));
    ee3=sqrt(dot( e3, e3, 3 ));
    
    E
    %Maxx_np(1,E)= enei(E);
    %Maxx_np(2,E)= max(max(ee));
    %  final plot
    figure;
    imagesc(x(:), y(:), ee); 
    axis equal on
    colormap hot( 255 );

    figure;
    imagesc(x(:), y(:), ee2);
    axis equal on
    colormap hot( 255 );

    
    figure;
    imagesc(x(:), y(:), ee3);
    axis equal on
    colormap hot( 255 );
    
    E
     
 end
 


 