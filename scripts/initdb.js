var dbadmin = db.getSiblingDB('cmm');
dbadmin.createUser(
  {
    user: "cmmuser",
    pwd: "cmm#secret123",
    roles: [ { role: "readWrite", db: "cmm" }]
  }
);
