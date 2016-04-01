function [data_balanced, data_validate, traincount, testcount] = near_miss(data,data_nonAEP)
nonAEPcount = length(data_nonAEP);
AEPcount = length(data);
for i=1:nonAEPcount
    for j=1:AEPcount
        dist(i,j) = norm(data_nonAEP(i,:)-data(j,:));
    end
end

sorted_distance = sort(dist,2);
% dist_in = sorted_distance(:,AEPcount-2:AEPcount)';
avg_distances = mean(sorted_distance(:,AEPcount-2:AEPcount)')';
[sorted,index] = sort(avg_distances);
traincount = ceil(0.75*AEPcount);
testcount = AEPcount - traincount;
data_balanced = data(1:traincount,:);
data_validate = data(traincount+1:AEPcount,:);
for i=1:traincount
    data_balanced = [data_balanced ; data_nonAEP(index(i),:)];
end

for i=1:testcount
   data_validate = [data_validate; data_nonAEP(index(i+traincount),:)]; 
end
end