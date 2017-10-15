function query(q){
    urls = [];
    request.get({
    url: "https://api.nytimes.com/svc/search/v2/articlesearch.json",
    qs: {
        'api-key': "223293e7d64544aa8e7eef843508be06",
        'q': q
    },
    }, function(err, response, body) {
        body = JSON.parse(body);
        console.log(body);
        for(var i = 0; i < 6; i++){
            urls.push(result.response.docs[i].web_url);   
        }
    })
    process.stdout.write(urls);
}