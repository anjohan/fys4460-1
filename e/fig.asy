settings.outformat = "pdf";
settings.prc = false;
settings.render = 16;
size(15cm,10cm,IgnoreAspect);
import three;
import graph3;
usepackage("mathpazo");

currentprojection=orthographic((-0.25,-3.5,0.5),up=Z);

file simulated_file = input("data/simulatedPs.dat");
real[][] simulatedPs = simulated_file.line();
int num_rhos = simulatedPs.length;
int num_Ts = simulatedPs[0].length;
write(num_rhos);
write(num_Ts);
real[][] eqTs = input("data/eqTs.dat").line();
real[] rhos = input("data/rhos.dat");

triple simulatedP(pair ij){
    int i = (int) ij.x;
    int j = (int) ij.y;
    return (rhos[i], eqTs[i][j], simulatedPs[i][j]);
}
write("test");

surface graf = surface(simulatedP, (0,0), (num_rhos-1,num_Ts-1),nu=num_rhos,nv=num_Ts,Spline);
draw(graf,surfacepen=material(diffusepen=red));

file fitted_file = input("data/fittedPs.dat");
real[][] fittedPs = fitted_file.line();

triple fittedP(pair ij){
    int i = (int) ij.x;
    int j = (int) ij.y;
    return (rhos[i], eqTs[i][j], fittedPs[i][j]);
}
write("test");

surface graf2 = surface(fittedP, (0,0), (num_rhos-1,num_Ts-1),nu=num_rhos,nv=num_Ts,Spline);
draw(graf2,material(blue,opacity=0.5));
axes3("$\rho\sigma^3$","$T/T_0$","$P/P_0$",min=(-0.2,-0.2,-0.2),max=(1.2,3.7,12),arrow=Arrow3());
