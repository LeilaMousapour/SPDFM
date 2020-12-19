%clc;
%clear;

%table of dielectric functions
epstab = {epsconst(1), epstable('gold.dat')};

p_gold1 = trisphere(256,20,'interp','curv');
p=comparticle(epstab, {p_gold1}, [2,1], 1);

figure;
plot (p,'EdgeColor','b');