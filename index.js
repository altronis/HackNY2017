            function query(q){
                urls = [];
                var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";
                url += '?' + $.param({
                'api-key': "223293e7d64544aa8e7eef843508be06",
                'q': q
                });
                $.ajax({
                url: url,
                method: 'GET',
                }).done(function(result) {
                console.log(result);
                for(i = 0; i < 6; i++){
                 urls.push(result.response.docs[i].web_url);   
                }
                }).fail(function(err) {
                throw err;
                });
                //return urls;
                process.stdout.write(urls);
            } 