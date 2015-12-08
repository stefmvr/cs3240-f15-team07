from django.shortcuts import render
from .models import MessageDB
from .models import UserAttributes
from .models import Groups
from .models import Folder
from .models import ReportModel
from .models import SingleFileModel
from django.template import RequestContext
from .forms import UploadReportForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Crypto.PublicKey import RSA
from Crypto import Random
from itertools import chain

# Create your views here.

def home_page(request):
    logout(request)
    # if(request.method == "POST"):
    #     cl = request.POST['cleardb']
    #     if(cl):
    #         users = User.objects.all()
    #         for u in users:
    #             u.delete
    return render(request, "login/home.html")

def delete_recursively(folder, owner):
	sub_folders = Folder.objects.filter(owner = owner, parent_folder = folder)
	for sf in sub_folders:
		delete_recursively(sf, owner)
	sub_reports = ReportModel.objects.filter(report_owner = owner, parent_folder = folder)
	for report in sub_reports:
		sub_files = SingleFileModel.objects.filter(file_report=report)
		for single_file in sub_files:
			single_file.delete()
		report.delete()
	folder.delete()

def has_same_name(newFolderName, otherFolders):
	for folder in otherFolders:
		if folder.name == newFolderName:
			return True
	return False

@login_required(login_url='/login/lg/')
def my_reports_page(request):
	parent = None
	message = ""
	if request.method == "POST":
		if "parentVar" in request.POST:
			parent = Folder.objects.get(pk=request.POST["parentVar"])
		if "folderChoice" in request.POST:
			parent = Folder.objects.get(pk=request.POST["whereToGo"])
		if "deleteFolder" in request.POST:
			to_delete = Folder.objects.get(pk=request.POST["whatToDelete"])
			delete_recursively(to_delete, request.user.username)
		if "deleteReport" in request.POST:
			report_to_delete = ReportModel.objects.get(pk=request.POST["reportToDelete"])
			report_to_delete.delete()
		if "changeName" in request.POST:
			if "parentVar" in request.POST:
				parent = Folder.objects.get(pk=request.POST["parentVar"])
			else:
				parent = None
			otherFolders = Folder.objects.filter(owner=request.user.username, parent_folder=parent.parent_folder)
			new_name = request.POST["folderName"].replace(" ", "_")
			if has_same_name(new_name, otherFolders):
				message = "That folder already exists"
			else:
				parent.name = new_name
				parent.save()
		if "folderToMake" in request.POST and request.POST["folderToMake"] != "":
			if "parentVar" in request.POST:
				parent = Folder.objects.get(pk=request.POST["parentVar"])
			new_name = request.POST["folderToMake"].replace(" ", "_")
			otherFolders = Folder.objects.filter(owner=request.user.username, parent_folder=parent)
			if has_same_name(new_name, otherFolders):
				message = "That folder already exists"
			else:
				f = Folder(name=new_name, parent_folder=parent, owner=request.user.username)
				f.save()
		if "backOut" in request.POST:
			parentParent = Folder.objects.get(pk=request.POST["parentVar"]).parent_folder
			print(parentParent)
			parent = parentParent
	reports = sorted(ReportModel.objects.filter(report_owner=request.user.username, parent_folder=parent), key=lambda report:report.report_title)
	report_file_list = [(each, SingleFileModel.objects.filter(file_report=each), each.report_groups.all(), each.report_sharedwith.all()) for each in reports]
	folderList = sorted(Folder.objects.filter(parent_folder = parent, owner=request.user.username), key=lambda folder:folder.name)
	return render(request, "login/my_reports.html", {"parent": parent, "user":request.user.username, "folders":folderList, "message":message, "reports":report_file_list})


@login_required(login_url='/login/lg/')
def upload_report(request):
	form = UploadReportForm()
	parent = None
	if request.method == 'POST':
		if "parentVar" in request.POST:
			parent = Folder.objects.get(pk=request.POST["parentVar"])
	usrAttr = UserAttributes.objects.get(user_name=request.user.username)
	groupList= sorted(usrAttr.groups.all(), key=lambda g:g.group_name)
	if usrAttr.is_site_manager:
		groupList=sorted(Groups.objects.all(), key=lambda g:g.group_name)
	userList = sorted(User.objects.all().exclude(username=request.user.username), key=lambda u:u.username)

	return render(request, "login/upload_report.html", {'user': request.user.username, 'form':form, 'parent': parent, 'userList': userList, 'groupList': groupList}, context_instance=RequestContext(request))

def minimum(int1, int2, int3):
	if int1 < int2:
		if int1 < int3:
			return int1
		return int3
	if int2 < int3:
		return int2
	return int3

def mintwo(int1, int2):
	if int1 < int2:
		return int1
	return int2

def levdistance(str1, str2):
	if str1.lower() == str2.lower():
		return 1
	m = len(str1)+1
	n = len(str2)+1
	matrix = []
	for i in range(m):
		matrix.append([])
		for j in range(n):
			matrix[i].append(0)
	for i in range(1, m):
		matrix[i][0] = i
	for j in range(1, n):
		matrix[0][j] = j
	for j in range(1, n):
		for i in range(1, m):
			if str1[i-1] == str2[j-1]:
				matrix[i][j] = matrix[i-1][j-1]
			else:
				matrix[i][j] = minimum(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + 1)
	return matrix[m-1][n-1]

@login_required(login_url='/login/lg')
def shared_with_me(request):
	if request.method == 'POST':
		print(request.POST)
		if "searchInReports" in request.POST:
			if request.POST["searchUsers"] != "" or request.POST["searchTerms"] != "":
				reports = None
				if UserAttributes.objects.get(user_name = request.user.username).is_site_manager:
					reports = ReportModel.objects.all()
				else:
					currAttr = UserAttributes.objects.get(user_name=request.user.username)
					currUser = User.objects.get(username=request.user.username)
					reports = list(set(chain(ReportModel.objects.filter(report_private=False), currUser.reportmodel_set.all(), ReportModel.objects.filter(report_owner=request.user.username))))
					for group in currAttr.groups.all():
						reports = list(set(chain(reports, group.reportmodel_set.all())))
				if request.POST["searchUsers"] != "":
					userSearchList = [s.strip() for s in request.POST["searchUsers"].split(',')]
					filterUserList = [item for sublist in [User.objects.filter(username=each) for each in userSearchList] for item in sublist]
					userNameList = [user.username for user in filterUserList]

					if len(userNameList) == 0:
						print("NO USERS")
						suggestedUsers = []
						potentialUsers = {}
						for searchUser in userSearchList:
							for user in [user.username for user in User.objects.all()]:
								if user not in potentialUsers:
									potentialUsers[user] = levdistance(user, searchUser)
								else:
									potentialUsers[user] = mintwo(levdistance(user, searchUser), potentialUsers[user])
						suggestedUsers = sorted(potentialUsers.items(), key = lambda a:a[1])
						print(suggestedUsers)
						suggestedUsers = [each[0] for each in suggestedUsers][:3]
						print(suggestedUsers)
						return render(request, "login/shared_with_me.html", {'user': request.user.username, 'message': "No users matched your username list.", 'suggestedUsers': suggestedUsers})
					reports = [report for report in reports if report.report_owner in userNameList]
				if request.POST["searchTerms"] != "":
					searchTermList = [s.strip() for s in request.POST["searchTerms"].split(',')]
					for term in searchTermList:
						print(term)
						reports = [report for report in reports if term.lower() in report.report_title.lower() or term.lower() in report.report_body.lower()]
				if len(reports) == 0:
					return render(request, "login/shared_with_me.html", {'user': request.user.username, 'message': "No reports matched your search."})

				report_file_list = [(each, sorted(SingleFileModel.objects.filter(file_report=each), key=lambda f: f.single_file.name), each.report_groups.all(), each.report_sharedwith.all()) for each in reports]
				return render(request, "login/shared_with_me.html", {'user': request.user.username, 'reports': report_file_list})
	#ELSE
	reports = None
	if UserAttributes.objects.get(user_name = request.user.username).is_site_manager:
		reports = ReportModel.objects.all().exclude(report_owner=request.user.username)
	else:
		currAttr = UserAttributes.objects.get(user_name=request.user.username)
		currUser = User.objects.get(username=request.user.username)
		reports = list(set(chain(ReportModel.objects.filter(report_private=False).exclude(report_owner=request.user.username), currUser.reportmodel_set.all().exclude(report_owner=request.user.username))))
		for group in currAttr.groups.all():
			reports = list(set(chain(reports, group.reportmodel_set.all().exclude(report_owner=request.user.username))))
	report_file_list = [(each, sorted(SingleFileModel.objects.filter(file_report=each), key=lambda f: f.single_file.name), each.report_groups.all(), each.report_sharedwith.all()) for each in reports]
	return render(request, "login/shared_with_me.html", {'user': request.user.username, 'reports': report_file_list})


@login_required(login_url='/login/lg/')
def edit_report(request):
	if request.method == 'POST':
		print(request.POST)
		usrAttr = UserAttributes.objects.get(user_name=request.user.username)
		groupList= sorted(usrAttr.groups.all(), key=lambda g:g.group_name)
		if UserAttributes.objects.get(user_name = request.user.username).is_site_manager:
			groupList = sorted(Groups.objects.all(),key=lambda g:g.group_name)
		userList = sorted(User.objects.all().exclude(username=request.user.username), key=lambda u:u.username)
		report = ReportModel.objects.get(pk=request.POST["reportSelected"])
		report_files = sorted(SingleFileModel.objects.filter(file_report=report), key=lambda file: file.single_file.name)

		parent = None
		if "parentVar" in request.POST:
			parent = Folder.objects.get(pk=request.POST["parentVar"])
		if "saveReportChanges" in request.POST:
			folderList = sorted(Folder.objects.filter(parent_folder=parent, owner=request.user.username), key=lambda folder:folder.name)
			form = UploadReportForm(request.POST, request.FILES)
			if form.is_valid():
				report.report_title = request.POST['report_title']
				report.report_body = request.POST['report_body']
				if 'report_private' in request.POST:
					report.report_private=True
				else:
					report.report_private=False
				report.save()
				if 'report_files' in request.FILES:
					for each in request.FILES.getlist('report_files'):
						newfile = SingleFileModel(single_file=each, file_report=report)
						newfile.save()
				report.parent_folder = parent
				report.save()

				reports = sorted(ReportModel.objects.filter(report_owner=request.user.username, parent_folder=parent), key=lambda report:report.report_title)
				report_file_list = [(each, SingleFileModel.objects.filter(file_report=each), each.report_groups.all(), each.report_sharedwith.all()) for each in reports]
				return render(request, "login/my_reports.html", {"parent": parent, "user":request.user.username, "folders":folderList, "reports":report_file_list})
			return render(request, 'login/edit_report.html', {'user': request.user.username, 'form': form, 'parent':parent, 'folders':folderList, 'report':report, 'report_files':report_files, 'groupList':groupList, 'userList':userList, 'report_groupList':sorted(report.report_groups.all(), key=lambda g:g.group_name), 'report_userList':sorted(report.report_sharedwith.all(), key=lambda u:u.username)})

		## IF WE'RE NOT SAVING THE REPORT CHANGES
		form = UploadReportForm(initial={"report_title":report.report_title, "report_body":report.report_body, "report_private":report.report_private})

		if "folderChoice" in request.POST:
			parent = Folder.objects.get(pk=request.POST["whereToGo"])
		if "backOut" in request.POST:
			parent = parent.parent_folder
		if "deleteFile" in request.POST:
			file_to_delete = SingleFileModel.objects.get(pk=request.POST["fileToDelete"])
			file_to_delete.delete()
			report_files = sorted(SingleFileModel.objects.filter(file_report=report), key=lambda file: file.single_file.name)
		if "addGroupSelector" in request.POST:
			if request.POST["addGroupSelector"] != "--default--":
				add_group = Groups.objects.get(pk=request.POST["addGroupSelector"])
				report.report_groups.add(add_group)
		if "addUserSelector" in request.POST:
			if request.POST["addUserSelector"] != "--default--":
				add_user = User.objects.get(username=request.POST["addUserSelector"])
				report.report_sharedwith.add(add_user)
		if "groupToRemove" in request.POST:
			remove_group = Groups.objects.get(pk=request.POST["groupToRemove"])
			report.report_groups.remove(remove_group)
			remove_group.reportmodel_set.remove(report)
		if "userToRemove" in request.POST:
			remove_user = User.objects.get(username=request.POST["userToRemove"])
			report.report_sharedwith.remove(remove_user)
			remove_user.reportmodel_set.remove(report)
		folders = sorted(Folder.objects.filter(owner=request.user.username, parent_folder=parent), key=lambda folder: folder.name)
		return render(request, "login/edit_report.html", {'user':request.user.username, 'form':form, 'parent':parent, 'folders':folders, 'report':report, 'report_files':report_files, 'userList':userList, 'groupList':groupList, "report_groupList":sorted(report.report_groups.all(), key=lambda g:g.group_name), "report_userList":sorted(report.report_sharedwith.all(), key=lambda u:u.username)})


@login_required(login_url='/login/lg/')
def submit_report(request):
	if request.method == 'POST':
		print(request.POST)
		form = UploadReportForm(request.POST, request.FILES)
		parent = None
		if 'parentVar' in request.POST:
			parent = Folder.objects.get(pk=request.POST['parentVar'])
		if form.is_valid():
			newreport = ReportModel(report_title = request.POST['report_title'], report_body = request.POST['report_body'], report_owner = request.user.username)
			if 'report_private' in request.POST:
				newreport.report_private=True
			else:
				newreport.report_private=False
			newreport.save()

			if 'report_files' in request.FILES:
				for each in request.FILES.getlist('report_files'):
					newfile = SingleFileModel(single_file=each, file_report=newreport)
					newfile.save()
			if 'addGroupSelector' in request.POST:
				if request.POST["addGroupSelector"] != "--default--":
					newreport.report_groups.add(Groups.objects.get(pk=request.POST["addGroupSelector"]))
			if 'addUserSelector' in request.POST:
				if request.POST["addUserSelector"] != "--default--":
					newreport.report_sharedwith.add(User.objects.get(username=request.POST["addUserSelector"]))
			newreport.save()

			if parent != None:
				newreport.parent_folder = parent
				newreport.save()
			reports = sorted(ReportModel.objects.filter(report_owner=request.user.username, parent_folder=parent), key=lambda report:report.report_title)
			report_file_list = [(each, SingleFileModel.objects.filter(file_report=each), each.report_groups.all(), each.report_sharedwith.all()) for each in reports]
			folderList = sorted(Folder.objects.filter(parent_folder=parent, owner=request.user.username), key=lambda folder:folder.name)

			return render(request, "login/my_reports.html", {'user': request.user.username, 'reports':report_file_list, 'folders':folderList, 'parent': parent}, context_instance=RequestContext(request))
		usrAttr = UserAttributes.objects.get(user_name=request.user.username)
		groupList= sorted(usrAttr.groups.all(), key=lambda g:g.group_name)
		if usrAttr.is_site_manager:
			groupList=sorted(Groups.objects.all(), key=lambda g:g.group_name)
		userList = sorted(User.objects.all().exclude(username=request.user.username), key=lambda u:u.username)
		return render(request, 'login/upload_report.html', {'user': request.user.username, 'form': form, 'parent':parent, 'userList':userList, 'groupList':groupList})

@login_required(login_url='/login/lg/')
def other_reports_page(request):
    pass

@login_required(login_url='/login/lg/')
def update_page(request):
    if request.method == 'POST':
        """if 'key' in request.POST
            dict = {}
            key = RSA.importKey(request.POST["key"].encode())
            dict.setdefault("publicKey", key.publickey().exportKey().decode())
            dict.setdefault("is_site_manager", False)
            bool = updateInfo(dict, request.user)
            if bool:
                message = "Attribute Created"
            else:
                message = "Attribute Updated"


                return render(request, "login/update.html", {'message':message})
        elifgenerate' in request.POST:"""
        if 'generate' in request.POST:
            random_generator = Random.new().read
            key = RSA.generate(1024, random_generator)
            private = key.exportKey()
            public = key.publickey().exportKey()
            updateInfo({"publicKey":public.decode(), "is_site_manager":False}, request.user)
            message = "This is your new private key: " + private.decode()
            return render(request, "login/update.html", {'message':message})


    return render(request, "login/update.html")

@login_required(login_url='/login/lg/')
def view_group(request):
	if request.method == 'POST':
		if "groupSelection" in request.POST:
			group = Groups.objects.get(pk=request.POST["groupSelection"])
			userList = group.userattributes_set.all().exclude(user_name=request.user.username)
			reports = group.reportmodel_set.all()
			report_file_list = [(each, sorted(SingleFileModel.objects.filter(file_report=each), key=lambda f:f.single_file.name)) for each in reports ]
			return render(request, "login/view_group.html", {"user": request.user.username, "group":group, "userList": userList, "reports":report_file_list})
		if "groupToDelete" in request.POST:
			group = Groups.objects.get(pk=request.POST["groupToDelete"])
			group.delete()
			return group_page(request)

@login_required(login_url='/login/lg/')
def group_page(request):
	if request.method == 'POST':
		print(request.POST)
		if 'creator' in request.POST:
			usr = UserAttributes.objects.get(user_name = request.user.username)
			gname = request.POST["groupToMake"]
			if gname != "":
				group = Groups(group_name=gname, group_creator=request.user.username)
				group.save()
				usr.groups.add(group)
		elif 'groupSelector' in request.POST:
			if request.POST["userSelector"] != "--default--" and request.POST["groupSelector"] != "--default--":
				addUsr = UserAttributes.objects.get(user_name = request.POST["userSelector"])
				group = Groups.objects.get(pk=request.POST["groupSelector"])
				groups = addUsr.groups.all()
				if group not in groups:
					addUsr.groups.add(group)
		elif 'groupToLeave' in request.POST:
			group = Groups.objects.get(pk=request.POST["groupToLeave"])
			usrAttr = UserAttributes.objects.get(user_name=request.user.username)
			group.userattributes_set.remove(usrAttr)
			usrAttr.groups.remove(group)
			if len(group.userattributes_set.all()) == 0:
				group.delete()
	groupList = sorted(UserAttributes.objects.get(user_name = request.user.username).groups.all(), key=lambda g:g.group_name)
	if UserAttributes.objects.get(user_name = request.user.username).is_site_manager:
		groupList = sorted(Groups.objects.all(), key=lambda g:g.group_name)
	groupUserPairs = [(each, sorted(each.userattributes_set.all(), key=lambda a: a.user_name)) for each in groupList]
	userList = sorted(User.objects.all().exclude(username=request.user.username), key=lambda u:u.username)
	return render(request, "login/groups.html", {"user": request.user.username, 'groups':groupUserPairs, "userList": userList, "groupList":groupList})

@login_required()
def site_manager_page(request):
    if UserAttributes.objects.get(user_name=request.user.username).is_site_manager:
        if request.method == "POST":
            if "userSelector" in request.POST:
                if request.POST["userSelector"] != "--default--":
                    makeManager = UserAttributes.objects.get(user_name = request.POST["userSelector"])
                    makeManager.is_site_manager = True
                    makeManager.save()
            if "suspendSelector" in request.POST:
                if request.POST["suspendSelector"] != "--default--":
                    suspendAccount = User.objects.get(username=request.POST["suspendSelector"])
                    suspendAccount.is_active = False
                    suspendAccount.save()
            if "reactivateSelector" in request.POST:
                if request.POST["reactivateSelector"] != "--default--":
                    reactivateAccount = User.objects.get(username=request.POST["reactivateSelector"])
                    reactivateAccount.is_active = True
                    reactivateAccount.save()
        inactiveList = User.objects.filter(is_active=False)
        activeList = User.objects.filter(is_active=True)
        makeList =  UserAttributes.objects.filter(is_site_manager=False)
        print("hi", makeList)
        for i in inactiveList:
            makeList = makeList.exclude(user_name = i)
        print("next", makeList, inactiveList, activeList)
        return render(request, "login/site_manager.html", {"makeList": makeList, "reactivateList":inactiveList, "suspendList":activeList})
    else:
        return render(request, "login/logged_in.html")


def updateInfo(dict, user):
    usr_att, created = UserAttributes.objects.get_or_create(user_name = user.username, defaults=dict)
    if not created:
        usr_att.publicKey = dict["publicKey"]
    usr_att.save()
    return created



def register_page(request):
    if request.method == 'POST':
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        private = key.exportKey()
        public = key.publickey().exportKey()
        if 'username' in request.POST and 'password' in request.POST:
            usr = request.POST["username"]
            ls = User.objects.all()
            makesiteman = False
            if (len(ls) == 0):
                makesiteman = True
            should_add = True
            for u in ls:
                if u.username == usr:
                    should_add = False
            if should_add:
                usr = User.objects.create_user(request.POST['username'],None, request.POST['password'])
                usr.save()
                usr = authenticate(username = request.POST['username'], password= request.POST['password'])
                if usr is not None:
                    login(request,usr)
                else:
                    error = ""
                    return render(request, "login/register.html", {'error': error})
                users = User.objects.all()
                updateInfo({"publicKey":public.decode(), "is_site_manager":makesiteman}, request.user)
                return render(request, "login/logged_in.html", {'user': request.user.username, 'siteManager': get_is_site_manager(request.user.username), 'key': private.decode()})
            else:
                error = "That Username is taken. Please try a different one."
                return render(request, "login/register.html", {'error': error})
        else:
            error = ""
            return render(request, "login/register.html", {'error': error})
    error = ""
    return render(request, "login/register.html", {'error': error})

def login_page(request):
    if request.user.is_authenticated():
        return render(request, "login/logged_in.html", {'user': request.user.username, 'siteManager': get_is_site_manager(request.user.username)})
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            usr = authenticate(username=request.POST["username"], password=request.POST["password"])
            if usr is not None:
                if usr.is_active:
                    login(request, usr)
                    return render(request, "login/logged_in.html", {'user': request.user.username, 'siteManager': get_is_site_manager(request.user.username)})
                else:
                    error = "Your account has been suspended."
                    return render(request, "login/login.html", {'error': error})
            else:
                error = "That Username and/or Password is incorrect."
                return render(request, "login/login.html", {'error': error})
        else:
            error = ""
            return render(request, "login/login.html", {'error': error})
    error = ""
    return render(request, "login/login.html", {'error': error})
@login_required(login_url='/login/lg/')
def message_page(request):
    recipients = User.objects.all()
    recipients = recipients.exclude(username=request.user.username)
    return render(request, "login/message.html", {'user': request.user, 'recipients':recipients})
def get_is_site_manager(username):
    usrAtt,created = UserAttributes.objects.get_or_create(user_name=username)
    is_manager = usrAtt.is_site_manager
    return is_manager

@login_required(login_url='/login/lg/')
def logged_in_page(request):
    return render(request, "login/logged_in.html", {'user': request.user.username, 'siteManager': get_is_site_manager(request.user.username)})

@login_required(login_url='/login/lg/')
def message_hub_page(request):
    #placeholder
    #query_results = Message.objects.all()
    if 'user' in request.POST and 'subject' in request.POST and 'body' in request.POST:
        usr = request.POST["user"]
        sub = request.POST["subject"]
        bod = request.POST["body"]
        enc = request.POST["encrypt"]

        msg = MessageDB.objects.createNew(sub, bod, enc, None, None, True)
        msg.save()
    messages = [("messageID1","testuser","IMPORTANT","THIS IS AN IMPORTANT MESSAGE"),("messageID2","testuser","False Alarm","Disregard Last Message"),("messageID3","testuser3","testuser","Always with the false alarms!"),("messageID4","testuser2","testuser's outbursts","testuser is really cutting into company time")]
    return render(request, "messages.html", {'user': request.user.username, 'messages': messages})

@login_required(login_url='/login/lg/')
def message_display_page(request):
    #query_results = MessageDB.objects.all()
    messages = [("messageID1","testuser","IMPORTANT","THIS IS AN IMPORTANT MESSAGE"),("messageID2","testuser","False Alarm","Disregard Last Message"),("messageID3","testuser3","testuser","Always with the false alarms!"),("messageID4","testuser2","testuser's outbursts","testuser is really cutting into company time")]
    return render(request, "messages.html", {'user': request.user.username, 'messages': query_results})

@login_required(login_url='/login/lg/')
def report_page(request):
	return render(request, "login/report_page.html", {'user': request.user.username})

def report(request):
    pass #do some shit
    return render(request, "report.html")

@login_required(login_url='/login/lg/')
def inbox_view(request):
    return render(request, "postman/inbox.html")



def delete_all(request):
    if request.method == 'POST':
        if 'password' in request.POST:
            usr = authenticate(username=request.user.username, password=request.POST["password"])
            if usr is not None:
                groupobjs = Groups.objects.all().filter(group_creator=request.user.username)
                groupobjs.delete()
                reportobjs = ReportModel.objects.all().filter(report_owner=request.user.username)
                reportobjs.delete()
                folderobjs = Folder.objects.all().filter(owner=request.user.username)
                folderobjs.delete()
                userobjs = UserAttributes.objects.all().filter(user_name = request.user.username)
                userobjs.delete()
                #usr = User.objects.get(request.user.username)
                usr.delete()

                #delete_recursively(to_delete, request.user.username)
                #do deleting here
                return render(request, "login/home.html")

            else:
                error = "That Password is incorrect."
                return render(request, "login/delete_all.html", {'error': error})
        else:
            error = ""
            return render(request, "login/delete_all.html", {'error': error})
    error = ""
    return render(request, "login/delete_all.html", {'error': error})

# def logged_in_reg_page(request):
#     if request.method == 'POST':
#         usr = request.POST["username"]
#         ls = User.objects.all()
#         should_add = True
#         for u in ls:
#             if u.username == usr:
#                 should_add = False
#         if should_add:
#             usr = User.objects.create_user(request.POST['username'],None, request.POST['password'])
#             usr.save()
#             users = User.objects.all()
#             return render(request, "login/logged_in.html", {'users': users})
#         else:
#             error = "That Username is taken. Please try a different one."
#             return render(request, "login/register.html", {'error': error})
#     error = ""
#     return render(request, "login/login.html", {'error': error})
#
# def logged_in_page(request):
#     if request.method == 'POST':
#         usr = authenticate(username=request.POST["username"], password=request.POST["password"])
#         if usr is not None:
#             if usr.is_active:
#                 login(request, usr)
#                 return render(request, "login/logged_in.html", {'user': request.user.username})
#             else:
#                 #placeholder
#                 return render(request, "login/logged_in.html")
#         else:
#             error = "That Username and/or Password is incorrect."
#             return render(request, "login/login.html", {'error': error})
#     error = ""
#     return render(request, "login/login.html", {'error': error})
#         # ls = User.objects.all()
#         # log = None
#         # for u in ls:
#         #     if u.user_name == usr:
#         #         log = u
#         #         break
#         # if log is not None:
#         #     if psw == u.password:
#         #         users = User.objects.all()
#         #         return render(request, "login/logged_in.html", {'users': users})
#         #     else:
#         #         error = "That password is Incorrect."
#         #         return render(request, "login/login.html", {'error': error})
#         # else:
#         #     error = "That Username is Incorrect."
#         #     return render(request, "login/login.html", {'error': error})
