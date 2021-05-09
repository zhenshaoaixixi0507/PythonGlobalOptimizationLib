function main()
clc;clear all;close all
fid = fopen('C:\Users\jingz\source\repos\PythonGlobalOptimizationLib\PythonGlobalOptimizationLib\PythonGlobalOptimizationLib\DataDownload\return.csv');
out = textscan(fid,'%s%f%f','delimiter',',');
fclose(fid);
data =out{1,1};
returndata=zeros(size(data,1),1);
for i=1:size(returndata,1)
    returndata(i,:)=str2double(data{i,1});
end
returndata=returndata(2:end,:);
residual=returndata-mean(returndata);
%Mdl = garch(1,1);
%EstMdl = estimate(Mdl,residual)
[optimizedpara,LLmin]=GARCHOptimize(returndata)
[sigma]=GenerateInSampleSigma(optimizedpara,returndata)
plot(sigma)
end

function[optimizedpara,LLmin]=GARCHOptimize(ret)
    residual=ret-mean(ret);
    fun = @(x)Loglik(x,residual);
    lb = [0.001;0.001;0.70];
    ub = [0.9999;0.99999;0.99999];
    A = [];
    b = [];
    Aeq = [0 1 1];
    beq = 0.9999;
    %x0=[0.02;0.05;0.65];
    x0=[0.01;0.005;0.85];
    options = optimoptions('fmincon','Display','iter');
    [optimizedpara,LLmin] = fmincon(fun,x0,A,b,Aeq,beq,lb,ub,[],options);
end
function[sumLL]=Loglik(para,residual)

 LL=zeros(size(residual,1),1);
 sigma=zeros(size(residual,1),1);
 sigmazero=mean(residual(1,:)^2);
 residualzero=sqrt(sigmazero);
 for i=1:size(LL,1)
     sigma(i,:)=para(1,:)+para(2,:)*residualzero^2+para(3,:)*sigmazero;
     LL(i,:)=0.5*log(2*pi)+0.5*log(sigma(i,:))+0.5*log(residual(i)^2/(sigma(i)));
     sigmazero=sigma(i,:);
     residualzero=residual(i,:);
 end
 sumLL=sum(LL);

end
function[sigma]=GenerateInSampleSigma(para,ret)
residual=ret-mean(ret);
sigmazero=mean(residual(1,:)^2);
residualzero=sqrt(sigmazero);
sigma=zeros(length(residual),1);
 for i=1:size(sigma,1)
     sigma(i,:)=para(1,:)+para(2,:)*residualzero^2+para(3,:)*sigmazero;
     sigmazero=sigma(i,:);
     residualzero=residual(i,:);
 end
end