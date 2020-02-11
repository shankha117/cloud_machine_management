var dbadmin = db.getSiblingDB('admin');
dbadmin.createUser(
  {
    user: "cmmuser",
    pwd: "cmm#secret123",
    roles: [ { role: "readWrite", db: "cmm" }]
  }
);
