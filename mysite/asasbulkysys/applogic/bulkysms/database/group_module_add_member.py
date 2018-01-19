          result={}
        
          try:
               contact_id=myjson["ContactID"]
               group_id=myjson["GroupID"]

          except Exception as e:
               #print "Content-type: text/html\n" 
               result["message"]="Error: '%s'. If the error persists contact the developer"%e
               return (json.JSONEncoder().encode(result)) 
               #sys.exit() 
          try:
               
               engine=db
               # create a Session
               Session = sessionmaker(bind=engine)
               session = Session()
               #Get person's name
               res2=session.query(AddressBook).filter(AddressBook.id==contact_id).first()
               person_name="%s %s"%(res2.first_name,res2.last_name)
               if res2 is None:
                    result["message"]="Error: The Person you are trying to assign to a group doesn't exist"
                    return (json.JSONEncoder().encode(result)) 
                  



               #get group was trying to be assigned to
               res2=session.query(Group).filter(Group.id==group_id).first()
               group_name="%s %s"%(res2.group_name,res2.group_description)

               if res2 is None:
                    result["message"]="Error: You are trying to assign '%s' to a group that doesn't exist"%person_name
                    return (json.JSONEncoder().encode(result))
               
                                  
               # querying for if a person has been assigned to this group before.
               res= session.query(GroupMember).filter(GroupMember.contact_id==contact_id).filter(GroupMember.group_id=group_id).first()
               if res is None:
                    #
                    new_group_member=GroupMember(contact_id,group_id)
                    session.add(new_group_member)
                    session.commit()
                    
               else:

                   result["message"]="Error:'%s' is arleady a member to '%s' group hence can't be assigned again"%(person_name,group_name) 
                   return (json.JSONEncoder().encode(result)) 
