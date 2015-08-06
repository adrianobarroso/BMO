%Calculates the main direction for each segment with wavelet (morlet type);
%the formulation of Lygre and Krogstad is used

%usa-se a convolucao com a wavelet complexa
a1=filter((out1-1i*out3)',1,co);
a2=filter((out1-1i*out3)',1,dd);
a3=filter((out1-1i*out3)',1,dc);

m4=2*dt/(m*0.375);
a1=a1(m:1024);
a2=a2(m:1024);
a3=a3(m:1024);

%espectros cruzados
z41=a1; z42=a2; z43=a3;
a4=m4*(z41.*conj(z41));
a8=m4*imag(z41.*conj(z42)); %a8 eh o coseno, projecao no eixo W-E;
a9=m4*imag(z41.*conj(z43)); %a9 eh seno projecao no eixo S-N;

a20=m4*(z42.*conj(z42));
a21=m4*(z43.*conj(z43));

a25=a20+a21;
a7=sqrt(a4.*a25);

a12=m4*real(z42.*conj(z43));

%o angulo c0 calculado eh em relacao ao eixo horizontal
c0=a8+j* a9;

c1=c0./a7;

c01=cos(c0);c02=sin(c0);           % Novos Parente
c03=angle(mean(c01)+j*mean(c02));  %
c03=ceil(c03*360/(2*pi));          %  

c2=(a20-a21+1i*2*a12)./a25;
c0=angle(c0)*360/(2*pi);
c0=ceil(c0);

c00=find(c0<=0);c0(c00)=c0(c00)+360;
pq=ceil(mean(c0));                 % Novos Parente 
pq=c03;                            %
g=find(pq<=0);pq(g)=pq(g)+360;     %

p1=(c1-c2.*conj(c1))./(1-(abs(c1)).^2);
p2=c2-c1.*p1;

tet2=zeros(1,m3+2);

%in order to avoid the ambiguity caused by 2teta the main 
%direction calculated by Fourier techniques is used 
%as a reference; the mem value is calculated in an interval
%of 100 degrees around this value;

%calculation for each segment
for kl=1:m3+2,
    
   %arredonda para cima
   p3=ceil(c0(kl));
   %p3=31;   
   d=(p3:p3+100);

   z1=1-p1(kl)*a26(d)-p2(kl)*a27(d);
   z1=z1.*conj(z1);z1=z1';
   
   %minimum of denominator is sufficient to
   %determine the maximum     
   p5=find(z1==min(z1)); p5=p5(1);
   p7=a30(p3+p5-1);
   
   %main direction (mem) for each segment
   tet2(1,kl)=grad1*p7;
   
   %z1=1./z1;z1=z1/max(z1);
   %if iwq==5,memarq(d',kl)=z1;arqc0(kl)=c0(kl);end;
   
end;


%spectrum for each segment
sp2=a4';
