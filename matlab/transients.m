function transLoc = transients(y, Fs, verbose)

transLoc = [];

%% accentuate peaks
% y = y .^ 2;

%% threshold away floor
% z = max(0, y - 0.5 * mean(y));

%% Apply initial gaussian to do light smoothing
N = 32;
H = fspecial('gaussian', [1 N], N/8);
lowPass = conv(H,y);
lowPass = lowPass(N/2:length(lowPass));

filtered_mean = mean(lowPass);

if verbose
    figure; plot(y, 'g'); title('LP 1');
    hold on; plot(lowPass);
    % plot(diff(lowPass));
    % plot([1 length(lowPass)], [0 0]);
    plot([1 length(lowPass)], [filtered_mean filtered_mean]);
    % figure; histogram(y);
end

%% Find transient peaks
isRising = true;
last_max = 1;
last_min = 1;
% transLoc = find(riseEdges);
transLoc = zeros(size(lowPass));
for i = 1:length(lowPass)-1
    s = lowPass(i);
    s_next = lowPass(i+1);
    if isRising && s > s_next
        isRising = false;
        last_max = i;
    elseif ~isRising && s < s_next
        isRising = true;

        cur_min = i;
        height = lowPass(last_max);
        prominence = height - max(lowPass(last_min), lowPass(cur_min))
        if height > filtered_mean && prominence > height/2
            transLoc(last_max) = true;
        end

        last_min = i;
    end
end

t = 1:length(y)-1;

if verbose
    figure; plot(t, y(t), t, lowPass(t), t, transLoc(t)*max(lowPass));
    title('Transients');
end

transLoc = find(transLoc);

end
