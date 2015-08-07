% Directional Analysis with Adaptive Techniques - DAAT
% Oceanographic Instrumentation Laboratory - LIOc-COPPE/UFRJ
% 
% Developed by:  Parente (1999)
%
% Last modification: 2015/07/30
%
%==========================================================================
% Observations
%
% 32 graus de liberdade
%
% Sensor GX3
% intervalo de amostragem = 1s
% tempo de registro = 20min
% numero de pontos por registro = 1024
% Dados: aceleracao Z e V, pitch e roll

% Sensor AXYS
% intervalo de amostragem = 0.78s
% tempo de registro = 20min
% numero de pontos por registro = 1312
% Dados: heave, dspNS, dspEW

clear, clc, close all

%% carrega arquivos

%table of sines and cosines for the mem method - tecnica de maxima entropia
%cria variaveis a23 e a24, com 360 colunas, que faz um circulo de 1 a -1
load lyg2.mat;

%gx3 e axys
% tebig = load('/home/hp/Dropbox/lioc/ambid/dados/TEBIG-axys_gx3_20140522/bmo.mat');

%aceleracao Z
% tebig1 = load('/home/hp/Dropbox/lioc/ambid/dados/TEBIG-axys_gx3_20140522/bmo1.mat');

%define variaveis (coluna 4 da gx3 que eh a 1 da axys)

%GX3 - TEBIG
% n1 = tebig1.stabacelZ(1,2:end) .* -9.81; %aceleracao z, corrige acelercao e 'g' para m/s^2
% n2 = tebig.gx3_ac_NS(4,:); %pitch
% n3 = tebig.gx3_ac_EW(4,:); %roll

%AXYS - TEBIG
% n1 = tebig.axys_heave(1,:);
% n2 = tebig.axys_disp_N(1,:);
% n3 = tebig.axys_disp_E(1,:);

%AXYS - RIO_GRANDE PNBOIA
% rio_grande_ax = '/home/hp/Documents/pnboia/dados/axys/rio_grande/hne/200905090600.HNE';
% [n1, n2, n3] = carregaaxys_hne(rio_grande_ax);

%AXYS - MEXILHAO - AMBIDADOS
% mexilhao_ax = '/home/hp/Dropbox/lioc/ambid/dados/Mexilhao-axys_20080718/200807180959.HNE';
% mexilhao_ax = 'C:\Users\lioc\Dropbox\lioc\ambid\dados\Mexilhao-axys_20080718.HNE';
% [n1, n2, n3] = carregaaxys_hne(mexilhao_ax);

%AXYS - RIO_GRANDE PNBOIA - Processamento em batelada
%ondas
pathname =     '/home/hp/Dropbox/pnboia/dados/bruto/triaxys/rio_grande/HNE/';
pathnamelist = '/home/hp/Dropbox/pnboia/dados/bruto/triaxys/listas/';

%carrega listas da axys
arq = load([pathnamelist,'list_RSMay09.txt']);
arqp = num2str(arq);
mes = 12;
ano = 2012;
local = 'Rio Grande/RS';
%declinacao magnetica
%dmag = -22; %santosrio grande
dmag = -23; %rio grande


%vento
time = load('/home/hp/Dropbox/pnboia/cfsr/time_RioGrande_200912.txt');
u = load('/home/hp/Dropbox/pnboia/cfsr/uCFSR_RioGrande_200912.txt');
v = load('/home/hp/Dropbox/pnboia/cfsr/vCFSR_RioGrande_200912.txt');

%retira dias repetidos
[time,ia,ic] = unique(time);
time = time(1:end-1);
u = u(ia(1:end-1));
v = v(ia(1:end-1));
 
ws = sqrt(u.^2 + v.^2);
wd = atan2(v,u) * 180 / pi; %vento de onde vem
wd = 270 - wd; %de onde vai para onde vem
wd(find(wd<0)) = wd(find(wd<0)) + 360;
wd(find(wd>360)) = wd(find(wd>360)) - 360;

%intervalo da amostragem (segundos)
fs = 1.28; %0.78;
nfft = 82; %64;

%% preparo dos arquivos

%cria matrizes de direcao, espec e energia com 10 linhas (representando 5
%faixas, cada uma com 2 direcoes; e 248 colunas representado o tempo (1 mes
%a cada 3 horas = 24/3*31)

dire = zeros(10,length(arqp)); %direcao (2 valores, ate  5 faixas)
espe = zeros(10,length(arqp)); %espectros (2 valores, ate 5 faixas)
energ = zeros(10,length(arqp)); %Hm0 + 4 energias (uma por faixa), valor zero, 4 picos (maiores)
% dire1 = dire;
% espe1 = espe;

%vetor de frequencias (verificar se esta correto)
dt = 1 / fs; %intervalo de amostragem
fny = 1 / (2 * dt); %freq de nysquit
x = dt * nfft; %auxiliar para o vetor de freq (pq 64)
f1 = 1/x:1/x:fny; %vetor de freq - verificar com parente
df=f1(2) - f1(1); %deltaf

%entrada para daat
% co = n1;
% dd = n3;
% dc = n2;

%mesmo circulo mas agora com com 460 colunas
a26 = [a23(311:360) a23 a23(1:50)];
a27 = [a24(311:360) a24 a24(1:50)];

%cria vetor de 0 a 360, iniciando em 311 e terminando em 50
a30 = [(311:360) (1:360) (1:50)];

% ??
grad1 = 0.0175;
grad2 = 180/pi;

% ????
%para o caso de usar matr1 (matriz de ocorrencias)
sa = [.5;.5;.5;.5;0.1];

% --------- Separação da faixa de frequencia ----------
% Espectro calculado com 32 graus de liberdade
% faixa 1    faixa 2     faixa 3     faixa 4  
% 3-21.33     6-10.66    10-6.40     16-3.76     
% 4-16.00     7-9.14     11-5.81     32-2.00     
% 5-12.80     8-8.00     12-4.92
%             9-7.11     13-4.57
%                        14-4.26
%                        15-4.00
%
% ------------------------------------------------------

%as wavelets serao calculadas para 3 ciclos - cada uma
%correspondendo a um pico do espectro de 1D - para um numero de pontos
%de uma wavelet de 3 ciclos multiplica--se o periodo acima por 3 e
%divide-se por 1 exemplo para 20 segundos.

%preparam-se entao as wavelets para os periodos das 5 faixas - com
%aproximacao para numero inteiro de pontos

%tamanho das wavelets, 3 vezes o periodo da faixa. caso nao tenha pico em
%uma faixa, calcula-se com o periodo central da faixa (dado pelo vetor
%picos1)

% ----------- 32 graus -------------------
% faixa 1: 64 48 38 
% faixa 2: 32 27 24 21
% faixa 3: 19 17 16 15 14 13 12
% faixa 4: 11 a 6

% ----------- ES 12 graus -------------------
% faixa 5: 9
% faixa 4: 21 21 20 19 19 18 18 17 17 16 16 15 15 15 14 14 14 13 13 13...
% faixa 3: 25 24 23 22
% faixa 2: 32 30 29 27 26
% faixa 1: 60 55 50 46 43 40 37 35 33

%o objetivo aqui é ter wavelets prontas para usa-las de acordo com
%o pico das faixas; caso nao haja pico em uma faixa, usa-se wavelets
%correspondentes a: faixa 1 - 14.28 s (55 pontos), faixa 2 - 9.52 s
%(37 pontos), faixa 3 - 7.76 s (30 pontos ) e faixa 4 - 3 s (12 pontos)

%cria vetor com o tamanho das wavelets

% ES - 12 gl
% mm=[60;55;50;46;43;40;38;35;33;32;30;29;27;26;25;24;23;22;21;21;20;19;...
%     19;18;18;17;17;16;16;15;15;15;14;14;14;13;13;13;12;12;12;12;12;11;...
%     11;11;11;11;10;10;10;10;10;10;9];

% ES - 32 gl
% mm=[64;50;48;44;38;32;30;27;25;24;21;19;18;17;16;15;14;13;12;11;11;10;10;9;9;8;8;8;7;7;...
%     7;7;6;6;6];

mm = 100:-1:6;
ms = [];

%cria vetores de dim 64,34
wavecos = zeros(64,34);
wavesen = wavecos;


for i = 1:length(mm)
    
    mn = mm(i); %wavelet atual
    ms = [ms;mn];
    
    %cria vetoer de -pi a pi no tamanho de mn, que é o tamanho da wavelet
    out2 = linspace(-3.14,3.14,mn);
    
    %cria janela de hanning para o tamanho da wavelet
    gau = hanning(mn);
    
    %cria wavelet cos ??
    out1 = gau'.* cos(3 * out2);
    %cria wavelet sen ??
    out3 = gau'.* sin(3 * out2);
    
    %coloca em cada coluna a wavelet de determinado tamanho. cria 34
    %wavelets ??
    wavecos((1:mn)',i) = out1';
    wavesen((1:mn)',i) = out3';
end

%% processamento

kkl = 0;
ik = length(arqp);

for ik = 1:ik
    
    kkl = kkl + 1;

    arq1=[pathname,arqp(ik,1:12),'.HNE'];

    disp([num2str(ik),' - ',num2str(arqp(ik,:))])
    
    %eta, etaNS, etaEW
    [n1, n2, n3]=loadhne(arq1);

    co=n1; %heave
    dc=n2; %dspNS
    dd=n3; %dspEW

    % ???
    %limite superior (3db) e limite inferior (3 db)
    % 1) 20     11.1
    % 2) 11.1   8.69
    % 3) 8.69   7.4
    % 4) 7.4    4.0
    % 5) 4.0    end
    % a wavelet sera gerada com as regras acima

    %serao calculadas as energias em cada faixa mencionada a partir do
    %espectro de uma dimensao considerando que o espalhamento entre cada
    %frequencia seja de 1/T

    %calculo do espectro de 1 dimensao
    ww55 = zeros(8,1);

    %calculo do espec (32 gl, 50% de overlap, alisamento de Welch)
    qq1 = spectrum(n1,nfft,nfft/2,'welch');

    %correcao do fator de escala
    qq1 = 2 * qq1(2:end,1); 

    %coloca a altura significativa (hm0) na primeira linha de ww55)
    ww55(1) = 4 * sqrt(sum(qq1) * df);

    %cria faixas de freq (periodo)
    faixa1 = [3:5]'; % 32 - 10.6 s
    faixa2 = [6:9]'; % 9.1 - 7.1 s
    faixa3 = [10:16]'; % 6.4 - 4.2 s
    faixa4 = [17:length(qq1)]'; % 4 - 1.6 s

    %espectros nas 4 faixas - 32 graus
    ww55(2) = sum(qq1(faixa1)); 

    ww55(3) = sum(qq1(faixa2)); 
    ww55(4) = sum(qq1(faixa3)); 
    ww55(5) = sum(qq1(faixa4)); 
    %picos1 é o valor da duracao da wavelet que será usada
    %correspondendo a 3 ciclos do periodo de interesse

    %quando nao ha pico na faixa:
    % 48--16s
    % 27--9s
    % 18--6s
    % 9--3s

    picos1=[48;27;18;9];

    %picos calculados a partir de qq1        

    %calcula a diferença do vetor qq1 (ex qq1(2)-qq1(1)=g1(1) )
    g1 = diff(qq1);
    %coloca 1 para valores >1, 0 p/ =0 e -1 p/<0
    g1 = sign(g1);
    %calcula diferença (g1 ficou com 30 elementos)
    g1 = diff(g1);
    %deixa o vetor com 31 elementos
    g1 = [0;g1];
    %acha o indice do pico
    g1 = find(g1 == -2);

    %serao calculados os 4 maiores picos

    %acha os valores de energia dos picos (g4) e indices dos picos (g5)
    [g4 g5] = sort(qq1(g1));

    %coloca os indices em ordem crescente de energia
    g6 = flipud(g1(g5));
    %inicia criacao do vetor de picos (coloca zeros caso soh tiver 1
    %pico)
    g6 = [g6;0;0;0;0];
    %escolhe os 4 primeiros (maiores) picos
    g6 = g6(1:4);
    %retira valores maiores que 14 (para tirar picos na alta freq??)
    g7 = g6(g6<14);

    %colocacao dos picos nas primeiras faixas para determinacao das
    %wavelets

    picos2 = zeros(4,1);

    for gh = 1:length(g7)

        %acha o indice da faixa1 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa1);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(1) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(1) = g7(gh);
            faixa1 = 0;
        end
            
        %acha o indice da faixa2 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa2);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(2) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(2) = g7(gh);
            faixa2 = 0;
        end
            
        %acha o indice da faixa3 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa3);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(3) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(3) = g7(gh);
            faixa3 = 0;
        end      

        %acha o indice da faixa4 que esta o valor g7(gh)
        g8 = find(g7(gh)==faixa4);
        
        %se não for matriz vazia, cria variavel logica: ans = 0 e
        %picos2(4) recebe o valor do pico, se nao nao faz nada
        isempty(g8);
        if ans == 0
            picos2(4) = g7(gh);
            faixa4 = 0;
        end      
            
    end

    %coloca o valor arredondado do pico * 3 em 'picos1'
    picos3 = picos1;    
    for gh = 1:4
         if picos2(gh) > 0
             picos1(gh) = round(3*1/f1(picos2(gh)));
         end
    end

    %valores dos picos para o arquivo final
    g5 = flipud(g5); %indices dos picos em ordem decrescente
    g5 = g1(g5); %indices dos picos em ordem crescente
    g5 = [g5;0;0;0;0]; %coloca zeros caso nao tiver picos?
    g5 = g5(1:4); %acha os 4 maiores picos
    g = find(g5>0); %acha valores de picos maior que zero
    g5(g) = 64./g5(g); %acha os periodos dos picos em ordem crescente 
    % (pq divide por 64?)

    %coloca os 4 periodos de pico na linha 7 a 10 do ww55
    ww55(7:10) = g5;

    % o valor do vetor ww5 (10 linhas) contem:
    % ww55 = [hm0, sp1, sp2, sp3, sp4, 0 , tp1, tp2, tp3, tp4]
    % hm0 - altura significativa
    % sp - somatorio do vetor de energia por faixa
    % tp - periodo de pico de cada faixa

    %preparo final do energ

    %coloca o valor de ww55 na coluna kkl do energ
    energ(:,kkl) = ww55;

    %serao calculadas 5 faixas com wavelets
    %para cada wavelet calcula-se uma matriz de direcao e desvio
    %padrao obtendo-se um D(teta) para cada faixa

    %faixas variando de 1 a 4
    for iwq = 1:4

        %acha dentro de 'mm' o indice do valor de picos1(iwq)
        g11 = find(picos1(iwq) == mm);

        %acha o valor da wavelet
        m=mm(g11(1));

        %cria variavel out com a wavelet com o tamanho de 'm' a ser
        %utilizada (pega as linhas e coluna da wavelet)
        out1=wavecos((1:m)',g11(1));
        out3=wavesen((1:m)',g11(1));

        %cria matriz de 1
        matr1=ones(20,90);

        %perguntar para o parente
        m1=1024-m;

        %parametros para o calculo de tet2 e sp2
        m3=m1;
        m1=m1-1;
        m3=m1;
        %m4=2*dt/(m*0.375); comentado pois eh calculado dentro de 'daat1'
        m2=m-1;

        %chama subrotina 'daat1'
        daat1

        %dire1(iwq,kkl)=mean(tet2*180/pi);
        daat2

    end;
end;  

%matriz de saida a cada 3 horas
dire1 = dire(:,1:3:end); 
espe1 = espe(:,1:3:end); 
energ1 = energ(:,1:3:end);

ws = ws(1:3:end);
wd = wd(1:3:end);

% ddir1=dire2; 
% ddir=ddir1;
% espe1=espe2;

%matriz de saida a cada 1 hora
% dire2=dire1;
% espe2=espe1;
% ddir1=dire2;
% ddir=ddir1;
% espe1=espe2;

%a pleds entra com o dire1 e espe1 que sao os dados espacados a cada 3h
pleds

