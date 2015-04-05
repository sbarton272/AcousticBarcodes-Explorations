function errs = countErrs(decoded, target)
m = length(target);
n = length(decoded);
if m > n
    decoded = [decoded, -ones(1,m-n)];
else
    target = [target, -ones(1,n-m)];
end

errs = sum(decoded ~= target);

end