from model.network.jsn_drop_service import jsnDrop
from time import gmtime  #  gmt_time returns UTC time struct frim 

class UserManager(object):
    current_user = None
    current_status = None
    current_screen = None
    chat_list = None

    def now_time_stamp(self):
        time_now = gmtime()
        timestamp_str = f"{time_now.tm_year}:{time_now.tm_mon}:{time_now.tm_mday}:{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
        return timestamp_str
 

    def __init__(self) -> None:
        super().__init__()

        self.jsnDrop = jsnDrop("6c420424-62ad-4218-8b1f-d6cf2115facd","https://newsimland.com/~todd/JSON")

        # SCHEMA Make sure the tables are  CREATED - jsnDrop does not wipe an existing table 
        result = self.jsnDrop.create("tblUser",{"PersonID PK":"A_LOOONG_NAME",
                                                "Password":"A_LOOONG_PASSWORD",
                                                "Status":"STATUS_STRING"})

        result = self.jsnDrop.create("tblChat",{"PersonID PK":"A_LOOONG_NAME",
                                                "DESNumber":"A_LOOONG_DES_ID",
                                                "Chat":"A_LOONG____CHAT_ENTRY",
                                                "Time": self.now_time_stamp()})

        # self.test_api()

    def register(self, user_id, password):
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}'") # Danger SQL injection attack via user_id?? Is JsnDrop SQL injection attack safe??
        if( "DATA_ERROR" in self.jsnDrop.jsnStatus): # we get a DATA ERROR on an empty list - this is a design error in jsnDrop
            # Is this where our password should be SHA'ed !?
            result = self.jsnDrop.store("tblUser",[{'PersonID':user_id,'Password':password,'Status':'Registered'}])
            UserManager.currentUser = user_id
            UserManager.current_status = 'Logged Out'
            result = "Registration Success"
        else:
            result = "User Already Exists"

        return result

    def login(self, user_id, password):
        result = None
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}' AND Password = '{password}'") # Danger SQL injection attack via user_id?? Is JsnDrop SQL injection attack safe??
        if( "DATA_ERROR" in self.jsnDrop.jsnStatus): # then the (user_id,password) pair do not exist - so bad login
            result = "Login Fail"
            UserManager.current_status ="Logged Out"
        else:
            UserManager.current_status = "Logged In"
            result = "Login Success"
        return result

    def chat(self,message):
        result = None
        if UserManager.current_status != "Logged In":
            result = "You must be logged in to chat"
        else: 
            user_id = UserManager.current_user
            des_screen = UserManager.current_screen
            api_result = self.jsnDrop.store("tblChat",[{'PersonID':user_id,
                                                        'DESNumber':des_screen,
                                                        'Chat':message,
                                                        'Time': self.now_time_stamp()}])
            if "ERROR" in api_result :
                result = self.jsnDrop.jsnStatus
            else:
                result = "Chat sent"

        return result

    def get_chat(self):
         result = None
         
         if UserManager.current_status == "Logged In":
            des_screen = UserManager.current_screen  
            api_result = self.jsnDrop.select("tblChat",f"DESNumber = '{des_screen}'")
            if not ('DATA_ERROR' in api_result) :
                UserManager.chat_list = self.jsnDrop.jsnResult
                result = UserManager.chat_list

         return result
         
                

        




    def test_api(self):
        result = self.jsnDrop.create("tblTestUser",{"PersonID PK":"Todd","Score":21})
        print(f"Create Result from UserManager {result}")

        self.jsnDrop.store("tblTestUser",[{"PersonID":"Todd","Score":21},{"PersonID":"Jane","Score":201}])
        print(f"Store Result from UserManager {result}")

        result = self.jsnDrop.all("tblTestUser")
        print(f"All Result from UserManager {result}")

        result = self.jsnDrop.select("tblTestUser","Score > 200") # select from tblUser where Score > 200
        print(f"Select Result from UserManager {result}")

        result = self.jsnDrop.delete("tblTestUser","Score > 200") # delete from tblUser where Score > 200
        print(f"Delete Result from UserManager {result}")

        result = self.jsnDrop.drop("tblTestUser")
        print(f"Drop Result from UserManager {result}")



        
