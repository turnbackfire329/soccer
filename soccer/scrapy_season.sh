if (( $# == 1))
then
    if [[ $1 -ge 1920 ]] ; then 
        scrapy crawl tmcom -s SEASON=$1 -s LOG_LEVEL=INFO
    else
        echo "Please enter a season greater than 1920"
    fi   
fi