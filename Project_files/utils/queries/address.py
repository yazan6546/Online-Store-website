from sqlalchemy import text

Insert_Address_Table = text("""
                            insert into Address (person_id, city, zip_code, street_address) 
                            values (:person_id, :city, :zip_code, :street);
                            """)


GET_ADDRESS_TABLE = text(""" 
                            select * from Address order by 1 desc;
                        """)

SELECT_ADDRESS_BY_Address_ID = text("""
                            select * from Address
                            where address_id = :id;
                            """)

SELECT_ADDRESS_BY_Person_ID = text("""
                            select * from Address
                            where person_id = :id;
                            """)

DELETE_FROM_ADDRESS = text("""
                            delete from Address
                            where address_id = :id;
                            """)

CREATE_ADDRESS_TABLE = text("""
                            create table if not exists Address(
                            address_id int not null auto_increment,
                            person_id int not null,
                            city varchar(255) not null,
                            zip_code varchar(255) not null,
                            street_address varchar(255) not null,   
                            primary key (address_id),
                            foreign key (person_id) references Person(person_id)
                            );
                            """)

DROP_ADDRESS_TABLE = text("""
                            drop table if exists Address;
                            """)