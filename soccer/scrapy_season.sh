if (( $# == 1))
then
    if [[ $1 -ge 2016 ]] ; then 
        scrapy crawl tmcom -s SEASON=$1 -s LOG_LEVEL=INFO
    else
        echo "Please enter a season between 2016 and 3000"
    fi   
fi