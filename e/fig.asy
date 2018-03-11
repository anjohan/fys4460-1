settings.outformat = "pdf";
settings.prc = false;
settings.render = 16;
size(15cm,10cm,IgnoreAspect);
import three;
import graph3;
usepackage("mathpazo");

currentprojection=orthographic((-0.15,-3.5,0.5),up=Z);
currentlight=light(-0.15,-3.5,1.5);
real myopacity=1;//0.801

real[][] simulatedPs = input("data/simulatedPs.dat").line();
int num_rhos = simulatedPs.length;
int num_Ts = simulatedPs[0].length;
real[][] eqTs = input("data/eqTs.dat").line();
real[] rhos = input("data/rhos.dat");

triple simulatedP(pair ij){
    int i = (int) ij.x;
    int j = (int) ij.y;
    return (rhos[i], eqTs[i][j], simulatedPs[i][j]);
}

surface graf = surface(simulatedP, (0,0), (num_rhos-1,num_Ts-1),nu=num_rhos,nv=num_Ts,Spline);
draw(graf,surfacepen=material(red+opacity(myopacity)));

file fitted_file = input("data/fittedPs.dat");
real[][] fittedPs = fitted_file.line();

triple fittedP(pair ij){
    int i = (int) ij.x;
    int j = (int) ij.y;
    return (rhos[i], eqTs[i][j], fittedPs[i][j]);
}

surface graf2 = surface(fittedP, (0,0), (num_rhos-1,num_Ts-1),nu=num_rhos,nv=num_Ts);
draw(graf2,surfacepen=material(blue+0.2*white+opacity(myopacity)),meshpen=black);
axes3("$\rho\sigma^3$","$T/T_0$","$P/P_0$",min=(-0.2,-0.2,-0.2),max=(1.2,3.7,12),arrow=Arrow3());
