function main()
clc;clear all;close all
fid = fopen('C:\Users\jingz\Source\Repos\PythonGlobalOptimizationLib\PythonGlobalOptimizationLib\PythonGlobalOptimizationLib\DataDownload\return.csv');
out = textscan(fid,'%s%f%f','delimiter',',');
fclose(fid);
data =out{1,1};
returndata=zeros(size(data,1),1);
for i=1:size(returndata,1)
    returndata(i,:)=str2double(data{i,1});
end
returndata=returndata(2:end,:);
optimizedpara=GARCHOptimize(returndata)
end

function[optimizedpara]=GARCHOptimize(ret)
    residual=ret-mean(ret);
    fun = @(x)Loglik(x,residual);
    lb = [0.0000001;0.0000001;0.0000001];
    ub = [0.0099999;0.99999;0.99999];
    A = [];
    b = [];
    Aeq = [0 1 1];
    beq = 0.9999;
    x0=[0.02;0.3;0.65];
    options = optimoptions('fmincon','Display','iter');
    optimizedpara = fmincon(fun,x0,A,b,Aeq,beq,lb,ub,[],options);
end
function[sumLL]=Loglik(para,residual)
if(para(2,:)+para(3,:)>=1)
    sumLL=9999999.99;
else
 LL=zeros(size(residual,1)-1,1);
 sigma=zeros(size(residual,1),1);
 sigma(1,:)=residual(1,:)^2;
 for i=1:size(LL,1)
     sigma(i+1,:)=para(1,:)+para(2,:)*residual(i,1)^2+para(3,:)*sigma(i,:);
     LL(i,:)=0.5*log(2*pi)+0.5*log(sigma(i+1,:))+0.5*log(residual(i+1)^2/((sigma(i+1)^2)));
 end
 sumLL=sum(LL);
end
end