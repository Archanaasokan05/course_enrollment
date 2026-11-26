import mysql.connector

class CourseEnrollment:
    def __init__(self):
        try:
            self.con=mysql.connector.connect(user="root",password="root",host="localhost",database="course_enrollment")
            print(self.con,"Connected Successfully")
        except:
            print("Failed to Connect")

    # Enroll student
    def create(self,name,course,duration,date,fee,status):
        try:
            c=self.con.cursor()
            if duration<=0:
                print("Duration must be a positive value")
                return
            if fee<0:
                print("Fee must be non-negative")
                return
            if status not in["Active","Completed","Cancelled"]:
                print("Invalid Status")
                return
            query="""insert into enrollments
                    (student_name,course_name,duration_months,enrollment_date,fee,status)
                    values(%s,%s,%s,%s,%s,%s)"""
            data=(name,course,duration,date,fee,status)
            c.execute(query,data)
            self.con.commit()
            print("Enrollment Added Successfully")
        except:
            print("Failed to Insert")

    # View enrollments(date)
    def read(self):
        try:
            c=self.con.cursor()
            query="select*from enrollments order by enrollment_date desc"
            c.execute(query)
            records=c.fetchall()
            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")
        except:
            print("Failed to Read")

    # View enrollments(fee)
    def sort_fee(self):
        try:
            c=self.con.cursor()
            query="select*from enrollments order by fee desc"
            c.execute(query)
            records=c.fetchall()
            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")
        except:
            print("Failed to Sort")

    # View enrollments(status)
    def filter(self,status):
        try:
            c=self.con.cursor()
            query="select*from enrollments where status=%s"
            data=(status,)
            c.execute(query,data)
            records=c.fetchall()
            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")
        except:
            print("Failed to Filter")

    # View enrollments(id)
    def retrieve(self,id):
        try:
            c=self.con.cursor()
            query="select*from enrollments where enrollment_id=%s"
            data=(id,)
            c.execute(query,data)
            record=c.fetchone()
            if record:
                print(record)
            else:
                print("No Records Found")
        except:
            print("Failed to Retrieve")

    # Search enrollment
    def search(self,name):
        try:
            cursor=self.con.cursor()
            query="""select*from enrollments where student_name like %s or course_name like %s"""
            data=('%'+name+'%','%'+name+'%')
            cursor.execute(query,data)
            records=cursor.fetchall()
            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")
        except:
            print("Failed to Search")

    # Update enrollment status
    def update(self,id,status,fee):
        try:
            if fee<0:
                print("Fee must be non-negative")
                return
            if status not in ["Active","Completed","Cancelled"]:
                print("Invalid Status")
                return
            c=self.con.cursor()
            query="update enrollments set status=%s,fee=%s where enrollment_id=%s"
            data=(status,fee,id)
            c.execute(query,data)
            self.con.commit()
            if c.rowcount>0:
                print("Record Updated Successfully")
            else:
                print("ID Not Found")
        except:
            print("Failed to Update")

    # Delete enrollment
    def delete(self,id):
        try:
            c=self.con.cursor()
            query="delete from enrollments where enrollment_id=%s"
            data=(id,)
            c.execute(query,data)
            self.con.commit()
            if c.rowcount>0:
                print("Record Deleted Successfully")
            else:
                print("ID Not Found")
        except:
            print("Failed to Delete")

    # Financial summary
    def summary(self):
        try:
            c=self.con.cursor()
            query="select count(*),sum(fee),avg(fee) from enrollments"
            c.execute(query)
            total,fees,average=c.fetchone()
            print("Total Enrollments:",total)
            print("Total Fees:",fees)
            print("Average Fee:",average)
            query="select status,count(*)from enrollments group by status"
            c.execute(query)
            records=c.fetchall()
            print("Status Count:")
            for row in records:
                print(row)
        except:
            print("Failed to Generate Summary")

    # close
    def close(self):
        self.con.close()
        print("Connection Closed")

p=CourseEnrollment()

while(1):
    print("\n1.Enroll Student")
    print("2.View All Enrollments")
    print("3.Search Enrollment")
    print("4.Update Enrollment")
    print("5.Delete Enrollment")
    print("6.Enrollment Summary")
    print("7.Exit")
    ch=int(input("Enter choice:"))

    if ch==1:
        n=input("Enter Student Name:")
        c=input("Enter Course Name:")
        d=int(input("Enter Duration in Months:"))
        date=input("Enter Enrollment Date(YYYY-MM-DD):")
        f=int(input("Enter Fee:"))
        s=input("Enter Status:")
        p.create(n,c,d,date,f,s)


    elif ch==2:
        print("1.View All(Recent Date First)")
        print("2.Filter by Status")
        print("3.Sort by Fee(Highest First)")
        choice = int(input("Enter choice:"))

        if choice==1:
            p.read()
        elif choice==2:
            s=input("Enter Status:")
            p.filter(s)
        elif choice==3:
            p.sort_fee()
        else:
            print("Invalid Choice")

    elif ch==3:
        print("1.Search by ID")
        print("2.Search by Name or Course")
        choice=int(input("Enter choice:"))

        if choice==1:
            id=int(input("Enter Enrollment ID:"))
            p.retrieve(id)
        elif choice==2:
            n=input("Enter Name or Course:")
            p.search(n)

    elif ch==4:
        id=int(input("Enter Enrollment ID:"))
        s=input("Enter New Status:")
        f=int(input("Enter New Fee:"))
        p.update(id,s,f)

    elif ch==5:
        id=int(input("Enter Enrollment ID:"))
        confirm=input("Are you sure? (yes/no):")

        if confirm=="yes":
            p.delete(id)
        else:
            print("Cancelled")
    elif ch==6:
        p.summary()
    elif ch==7:
        p.close()
        exit()
    else:
        print("Invalid Choice")
