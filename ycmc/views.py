from django.http import HttpResponse
from .ycmc_core import CodeDetector
from rest_framework.views import APIView
from github import Github,GithubException
from rest_framework.response import Response
from rest_framework import status
import uuid
import json
from .models import DetectInformation
# Create your views here.


class HomeView(APIView):
    def get(self,request):
        data = {
"repo1_url" : "Sankalpa-Acharya/asktorobo",
"repo2_url":"Sankalpa-Acharya/karya"

}
        return Response(data)
   
    def post(self,request):
        repo1_url = request.data.get('repo1_url')
        repo2_url = request.data.get('repo2_url')

        if (isinstance(request.data,dict)):
            try:
                y1 = CodeDetector(repo1_url, 'repo1')
                ex1,files1,_ = y1.get_repo_files()
                y2 = CodeDetector(repo2_url, 'repo2')
                ex2,files2,_ = y2.get_repo_files()
                common_file_extension = CodeDetector.get_similar_extension(y1,y2)
                file1_common = {ext:files1.get(ext)  for ext in common_file_extension}
                file2_common = {ext:files2.get(ext)  for ext in common_file_extension}
            except Exception as e:
                return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
            if ((repo1_url and repo1_url)!=None):
                return Response({repo1_url:file1_common,repo2_url:file2_common,"uuid":uuid.uuid4()},status=status.HTTP_200_OK)
            return Response({'error':'Something went wrong, we couldn\'t process'},status=status.HTTP_400_BAD_REQUEST)

class DetectHome(APIView):
    def get(self,request,pid):
        return Response({'message':'get page of detect route'}
)
    # check if the repo are same and data is provided then don't resend instead re-check
    def post(self,request,pid):
        files = request.data
        data = DetectInformation.objects.filter(_id=pid)
        if(len(data)!=0):
            return Response(json.loads(data[0].data))
            
        if (isinstance(files,dict)):
            repo1_url = list(files.keys())[0]
            repo2_url = list(files.keys())[1]
           
            if(not files[repo1_url] or not files[repo2_url]):
                return Response({'error':'no files provided'})
            try:
                y1 = CodeDetector(repo1_url, 'repo1')
                y2 = CodeDetector(repo2_url, 'repo2')
                _,__,branch1 = y1.get_repo_files()
                _,__,branch2 = y2.get_repo_files()
                ex = set(files[repo1_url].keys()).intersection(set(files[repo2_url].keys()))
                common_extension = ex.intersection(CodeDetector.get_similar_extension(y1,y2))
                repo1_files = files[repo1_url]
                repo2_files = files[repo2_url]
                for i in common_extension:
                    if i in repo1_files:
                        y1.files+= [*repo1_files[i]]
                    if i in repo2_files:    
                        y2.files+= [*repo2_files[i]]
                files_info,files_mapper = y1.download_files(files,common_extension)
                files_info2,files_mapper2 = y2.download_files(files,common_extension)
                output = CodeDetector.similarities_checker(
                        {**files_info, **files_info2}, common_extension, {**files_mapper, **files_mapper2},
                        {'repo1':branch1,'repo2':branch2}
                        
                        )
                y1.delete_files()
                y2.delete_files()
            except Exception as e:
                return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        output[0].insert(0,repo1_url)
        output[0].insert(0,repo2_url)
        DetectInformation.objects.create(_id=pid,repo1=repo1_url,repo2=repo2_url,data=json.dumps(output))
        return Response(output)

