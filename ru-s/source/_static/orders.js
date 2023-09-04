urlp=[]; s=location.toString().split('?');s=s[1].split('&');for(i=0;i<s.length;i++){u=s[i].split('=');urlp[u[0]]=u[1];}
const hp_appId = urlp['Shp_appId']
const hp_orderId = urlp['Shp_orderId']

//.A. - application
//.S. - supporting

if(hp_orderId.includes(".S.")){
    window.location.replace("./support-success.html");
}
