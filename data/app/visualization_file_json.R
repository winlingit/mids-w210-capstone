library(data.table)
library(rjson)
# 
# # Prepare SIG data
# sig_grouped = fread('sig_grouped.csv')
# sig_grouped$V1 = NULL
# 
# mapping = fread('mapping.csv')
# mapping = mapping[!is.na(mapping$categoryId)]
# 
# unique_cats = unique(mapping$categoryId)
# rating_cats = fread('rating_categories.csv')
# 
# 
# sig_grouped = sig_grouped[sig_grouped$categoryId %in% unique_cats,]
# mapping = mapping[mapping$categoryId %in% unique_cats,]
# 
# temp = dcast(sig_grouped, candidateId~categoryId, value.var="rating")
# temp2 = melt(temp, id.vars="candidateId")
# temp2$value[is.na(temp2$value)] = 0
# 
# sig_data = temp2
# names(sig_data) = c("votesmart_id", "categoryId", "rating")
# temp4 = merge(sig_data, rating_cats)
# 

# Prepare PAC Data
pac_data = fread('member_vpp_dw_pac.csv')
ids = unique(pac_data$opensecrets_id)
ft = pac_data[,.(opensecrets_id, Industry, Amount)]

ft = ft[, .(Amount = sum(Amount)), by=list(opensecrets_id, Industry)]

temp = dcast(ft, opensecrets_id~Industry, value.var="Amount")
ft = melt(temp, id.vars="opensecrets_id")

names(ft) = c("opensecrets_id", "Industry", "Total")
ft$Total = as.numeric(ft$Total)
ft[is.na(ft$Total)]$Total = 0
ft = ft[ft$opensecrets_id!="",]

# Create unique member data and join to fact table

cd = unique(pac_data[,.(opensecrets_id,state, party, type, dw_nominate)])
cd = cd[,.(dw_nominate = mean(dw_nominate)), by=list(opensecrets_id, state, party, type)]
names(cd) = c("opensecrets_id", "State", "Party", "Rep Type", "DW_Nominate")

df = merge(ft, cd, on="opensecrets_id")

members = fread("legislators-current.csv")[,.(opensecrets_id, first_name, last_name)]
members[,name := paste(first_name, last_name)]
members$last_name = NULL
members$first_name = NULL

df = merge(df, members)

# Find top 20 industries by PAC spending
# Create two separate files for it

ind_sums = df[,sum(Total), by=Industry]
setorder(ind_sums, -V1)
top_inds = ind_sums$Industry[1:20]

df$opensecrets_id = NULL

limited = df[Industry %in% top_inds,]

# Write to JSON


out = toJSON(unname(split(df, 1:nrow(df))))
cat(out, file="data_viz.json")

out = toJSON(unname(split(limited, 1:nrow(limited))))
cat(out, file="data_viz_limited.json")

