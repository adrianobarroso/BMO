%Select the segments for the directional spectrum composition
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Prepared by C.E. Parente
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

it=2*(iwq-1)+1;

q1=cos(tet2);q2=sin(tet2);

%Preparing ensembles of m segments advancing one sample

%fr3 is a matrix of cos and fr5 of sines of the segments whose direction
%stability will be investigated
%fr4 is the spectrum matrix

pm=length(round(m/2):m1-(m-round(m/2)));
fr3=zeros(round(m/2),pm);
fr5=fr3;fr4=fr3;
for ip=1:round(m/2),
   fr3(ip,:)=q1(ip:m1-(m-ip));
   fr5(ip,:)=q2(ip:m1-(m-ip));
   fr4(ip,:)=sp2(ip:m1-(m-ip));
end;

%using the mean and the standard circular deviation
%to select the segments with a given stability
fr2a=mean(fr3);fr2b=mean(fr5);
r=sqrt(fr2a.^2+fr2b.^2);

%circular deviation
fr9=sqrt(2*(1-r));

%fr99=fr9;fr2aa=fr2a;fr3a=fr3;q1a=q1;tet2a=tet2;

%espectro medio por coluna
%fr45=mean(fr4); %henrique comentou pois nao esta sendo usado o 'er5'
fr2=angle(fr2a+1i*fr2b);

%correcao de direcao para valores maiores e menores que 0 e 2pi
g=find(fr2<0);fr2(g)=fr2(g)+2*pi;
g=find(fr2>2*pi);fr2(g)=fr2(g)-2*pi;

%g fica com o numero de colunas de fr2
g=size(fr2);g=g(2);

%a15=0; %henrique comentou pois nao esta sendo usado o 'er5'

%criterio de aceitacao do desvio padrao dos segmentos
zm = 0.5; %series da axys (boas)
%zm = 1.2; %series do gx3 (ruins)

%segments with values of the standard deviations smaller
%than the threshold are selected

%er5=mean(fr4); %henrique comentou pois nao esta sendo usado o 'er5'

b7=find(fr9<zm);

%selected directions(segments)
a15=fr2(b7);

%selected spectrum values
er4=mean(fr4(:,b7));


% a15 is the the final vector with selected direction values
a15=ceil(a15*360/(2*pi)); %passa para graus

%a15=90+a15-14;(waverider de Santa Catarina)
%a15=90+a15-21;%(waverider de Arraial)
% BOIA ES dmag -23
a15 = a15 + dmag;

%Correcting for declination
% usando EtaEW e EtaNS ja esta descontado a dmag
a15=270-a15;

%correcao de direcao para valores maiores e menores que 0 e 360
g=find(a15<0);a15(g)=a15(g)+360;
g=find(a15>360);a15(g)=a15(g)-360;

%caixas para acumulo e obtencao de D(teta)
w1=zeros(360,1);%direcao principal
w2=zeros(360,1);%ocorrencias
a16=a15;

%w4=w2;%direcao sem overlapping
%w2a=w2;%ocorrencias sem    overlapping

%caso existam valores selecionados
if length(a15)>1
    
    b1=find(a15<=0);a15(b1)=a15(b1)+360;
    b1=find(a15<=0);a15(b1)=a15(b1)+360;
    b1=find(a15>360);a15(b1)=a15(b1)-360;
    b1=find(a15>360);a15(b1)=a15(b1)-360;

    %algoritmo para reduzir overlapping para
    %calculo de spread
    %   [p1 p2]=sort(er4');p1=flipud(p1);
    %   p2=flipud(p2);

    %      maxdir=[p2(1)];
    %   for i=2:length(p2),
    %      q=p2(i);
    %      q1=abs(maxdir-p2(i));
    %      g=find(q1<(m/2));
    %      isempty(g);
    %      if ans==1,
    %         maxdir=[maxdir;p2(i)];
    %      end;
    %   end

    %direcao e espectro sem overlapping
    %  a16=a15(maxdir);
    %  er5=er4(maxdir);
    a15 = round(a15);
    
    %storing spectrum values in 1 degree boxes;
    for k=1:length(a15)
        
        bb=a15(k);
        w1(bb)=w1(bb)+sp2(k);
        w2(bb)=w2(bb)+1;
        
    end;
end;

%filtrando w1 para determinar D(teta)
[b,t1]=butter(6,0.075);
xx=[w1(321:360);w1;w1(1:40)];

x=filtfilt(b,t1,xx);
x=x(41:400);
g=find(x<0);x(g)=0;

%calculando 2 direcoes
g1=diff(x);g1=sign(g1);g1=diff(g1);
g1=[0;g1];g1=find(g1==-2);

[p1 p2]=sort(x(g1));
isempty(p1);

if ans==0
    
    p=[flipud(g1(p2));0];p=p(1:2);
    e=[flipud(p1);0];e=e(1:2);
    
end

%jogo fora valores espacados de menos de 50 graaus
if abs(p(1)-p(2))<20
    
    e(2)=0;
    p(2)=0;
    
%ou pequenos    
elseif e(2)<0.1*e(1)
    
    e(2)=0;
    p(2)=0;
end;

%normalizacao com as energias das faixas obtidas do espectro 1D
z1=ww55(iwq+1);
p=[p;0;0;0];p=p(1:2);
e=[e;0;0;0];e=e(1:2);
e=e*z1/sum(e);
dire(it:it+1,kkl)=p;
espe(it:it+1,kkl)=e;






