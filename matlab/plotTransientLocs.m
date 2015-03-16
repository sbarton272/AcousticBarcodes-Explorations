function plotTransientLocs(trans, y, Fs)
% Plot energy

y = y.^2;
t = linspace(0,length(y)/Fs,length(y));
transPlt = zeros(1,length(y));
transPlt(trans) = -max(y)/5;

figure;
hold on;
plot(t, y);
stem(t,transPlt, 'r');
hold off;
end