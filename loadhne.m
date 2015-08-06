% carrega dados .hne

%function [dados_hne,ano,mes,dia,hora,minuto,sdata,stime]=carregaaxys_hne(arq1)

function [heave etaNS etaEW]=carregaaxys_hne(arq1)

fid=fopen(arq1,'r');

% Pula 3 linhas com comentarios do cabecalho (no arquivo *.HNE)
fgetl(fid);fgetl(fid);fgetl(fid);
% Leitura da linha com data
linha=fgetl(fid);
datatexto=[linha(17:18) ,'-',linha([13:15]),'-',linha(8:11),linha(19:end),':00'];
tempo = datenum(datatexto);

sdata=datestr(tempo,24); % formato 24 = 'dd/mm/yyyy' 01/03/2000
stime=datestr(tempo,15); % formato 15 = 'HH:MM'      15:45

[ano mes dia hora minuto] = datevec(tempo);

fclose(fid);

% pula o cabe�alho e le com o textread direto as series de heave, etaNS e etaEW
[lixo,heave,etaNS,etaEW]=textread(arq1,'%f%f%f%f','headerlines',11);

dados_hne=[heave etaNS etaEW];


