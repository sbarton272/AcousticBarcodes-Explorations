function fltY = preFilter(y, verbose)

N = 256;
W = .1;

b = fir1(N, W, 'high');

if verbose
    figure;
    freqz(b,1);
end

fltY = filter(b,1,y);

end