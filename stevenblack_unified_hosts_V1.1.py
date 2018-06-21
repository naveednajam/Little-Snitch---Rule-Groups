import os
import time
import urllib2

def main():

	#target_url='https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'
	target_url='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts'
	output_dir='unified_host_f_g_p'
	output_script='stevenblack'
	description=''
	name='Steven Black'
	script_number=0
	rule_count=0
	
	#booleans
	description_ends=False
	first_rule=True
	

	begin='{\n'+'	"description" : "'+description+'",\n	"name" : "'+name+'",\n'+'	"rules" :\n	[\n'
	end='    ]\n}'
	
	rule_start='        {\n'
	rule_subsequent_start=',\n        {\n'
	rule_action='            "action" : "deny",\n'
	rule_creationDate='            "creationDate" : '+str(time.time())+',\n'
	rule_modificationDate='            "modificationDate" : '+str(time.time())+',\n'
	rule_notes='            "notes" : "",\n'
	rule_owner='            "owner" : "me",\n'
	rule_process='            "process" : "any",\n'
	rule_remote_domain='            "remote-domains" : "'+"domain"+'"\n'
	rule_end='        }'


	f_host=urllib2.urlopen(target_url)
	#f= open(output_script+str(script_number),"w+")
	fl =f_host.readlines()
	for line in fl:
		line=line.strip()
		#print(line)
		if (line.startswith('# Date:') or line.startswith('# Number')) and not line.endswith('=') and description_ends==False:
			description= description+line.split('#')[1]+' , '
		elif line.startswith('#') and line.endswith('=') and description_ends==False:
			description_ends=True
			begin='{\n'+'	"description" : "'+description+'",\n	"name" : "'+name+'",\n'+'	"rules" :  [\n'
			f_host.close()
			break
    			
	#print(begin)
	#quit()
	f_host=urllib2.urlopen(target_url)
	fl =f_host.readlines()
	current_number=-1
	for line in fl:
		line=line.strip()
		#print(line)
		if  script_number > current_number :
			global f
			file_name=output_script+str(script_number)+'.lsrules'
			
			if os.path.exists(os.path.join(os.getcwd(),output_dir)) :
				dir_path=os.path.join(os.getcwd(),output_dir)
				
				f= open(os.path.join(dir_path,file_name),"w+")
			else: 
			
				try:
					os.makedirs(os.path.join(os.getcwd(),output_dir))
				except OSError as obj:
					error = obj.strerror+os.path.join(os.getcwd(),output_dir)
					print("%d: %s" %(obj.errno,error))
					pass
				dir_path=os.path.join(os.getcwd(),output_dir)
				f= open(os.path.join(dir_path,file_name),"w+")
			
			#f= open(file_name,"w+")
			begin='{\n'+'	"description" : "'+description+'",\n	"name" : "'+file_name+'",\n'+'	"rules" :  [\n'
			f.write(begin)
			current_number=script_number
			print('Opened new file: '+ output_script+str(script_number)+'.lsrules')
		
		if (line.startswith('#') or line.startswith('# Start') or line.startswith('#<') ) and not (line.startswith('#0.0.0.0') or line.startswith('# 0.0.0.0') or line.startswith('#</') or line.startswith('# start')) and not ((line.endswith('=') or line.endswith('#') or line.endswith('.') or line.endswith(':'))):
			rule_notes='            "notes" : "'+line.split('#')[1]+'",\n'
			if line == '# or C:\Windows\System32\drivers\etc\hosts' :
				rule_notes='            "notes" : "Start Badd-Boyz-Hosts",\n'
			elif line == '# See the License for the specific language governing permissions and' :
				rule_notes='            "notes" : "Start lightswitch05",\n'
			elif line == '# Podejrzane i/lub strony polaczone z innymi oszustwami' :
				rule_notes='            "notes" : "Start KADhosts",\n'
				
		elif (line.startswith('#</') and line.endswith('>')):
			rule_notes='            "notes" : "",\n'
		elif line.startswith('0.0.0.0') and not (line.endswith('0.0.0.0')):
			domain=line.split('0.0.0.0')
			if first_rule:	
				f.write(rule_start)
				first_rule=False
				#print('Adding first rule: '+str(str(rule_count)))
			else :
				f.write(rule_subsequent_start)
				#print('Adding subsequent rule: '+str(rule_count))
			f.write(rule_action)
			rule_creationDate='            "creationDate" : '+str(time.time())+',\n'
			f.write(rule_creationDate)
			rule_modificationDate='            "modificationDate" : '+str(time.time())+',\n'
			f.write(rule_modificationDate)
			f.write(rule_notes)
			f.write(rule_owner)
			f.write(rule_process)
			rule_remote_domain='            "remote-domains" : "'+str(domain[1].strip())+'"\n'
			f.write(rule_remote_domain)
			f.write(rule_end)
			rule_count+=1
			if rule_count == 10000 :
				print("10,000 rules completed, closing file")
				f.write(end)
				f.close()
				script_number+=1
				rule_count=0
				#print("rule-count reset done")
	if rule_count<10000 :				
		f.write(end)
		f.close()
		print(str(rule_count)+' completed, closing the file')
	f_host.close()
	print('conversion completed')
	quit()
    				   
if __name__== "__main__":
  main()