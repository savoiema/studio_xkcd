#!/usr/bin/env bash

tmp__working=$(pwd)

if [[ ! -d ../mysql ]]; then
    # lets do some setup
    cd ..
    mkdir mysql
    cd mysql
    tmp__mysql_data_folder=$(pwd)
    cd ../app
fi

# Create a network for the project
# --------------------------------
docker network create --subnet=172.18.0.0/16 studio_xkcd

# Create MySQL DB image
# ---------------------
docker run \
 -p 0.0.0.0:3306:3306 \
 -v ${tmp__mysql_data_folder}:/var/lib/mysql \
 --net studio_xkcd \
 --ip 172.18.0.2 \
 --name=mysql1 \
 -d mysql/mysql-server:latest

tmp__root_pw=$(docker logs mysql1 2>&1 | grep GENERATED | awk '{print $5}')

# Build python image
# ------------------
docker build . -t studio_xkcd

# Build redis image
# -----------------
cd ./scripts/redis
docker build . -t redis
cd ../../

cp ${tmp__working}/scripts/clean_up.sh ../clean_up.sh
cp ${tmp__working}/scripts/schema.sql ../mysql/studio_xkcd_schema.sql

# Configure the DB
# ----------------

cat << EOF > ../mysql/studio_xkcd_setup.sh
#!/usr/bin/env bash

mysql -u root -pPASSWORD < /var/lib/mysql/studio_xkcd_schema.sql

EOF

echo "Password is: "${tmp__root_pw}
echo "Run the commands below:"
echo "alter user 'root'@'localhost' identified by 'PASSWORD';"
echo "flush privileges;"
echo "exit"
echo
docker exec -it mysql1 mysql -uroot -p
docker exec -it mysql1 bash /var/lib/mysql/studio_xkcd_setup.sh

# Start Redis Instance
# --------------------
docker run \
 -p 0.0.0.0:6379:6379 \
 --net studio_xkcd \
 --ip 172.18.0.4 \
 --name=redis1 \
 -d redis:latest

# Start Python Instance
# ---------------------
docker run \
 -p 0.0.0.0:8086:8086 \
 --net studio_xkcd \
 --ip 172.18.0.3 \
 --name=studio_xkcd1 \
 -d studio_xkcd
