import os
import time
import urllib2

def main():
	base='https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'
	base_fakenew='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts'
	base_gambling='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling/hosts'
	base_porn='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts'
	base_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social/hosts'
	base_fakenews_gambling='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts'
	base_fakenews_porn='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-porn/hosts'
	base_fakenews_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-social/hosts'
	base_gambling_porn='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn/hosts'
	base_gambling_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-social/hosts'
	base_porn_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-social/hosts'
	base_fakenews_gambling_porn='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts'
	base_fakenews_gambling_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-social/hosts'
	base_fakenews_porn_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-porn-social/hosts'
	base_gambling_porn_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn-social/hosts'
	base_fakenews_gambling_porn_social='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts'
	
	hostfiles=[base,
					base_fakenew,
					base_gambling,
					base_porn,
					base_social,
					base_fakenews_gambling,
					base_fakenews_porn,
					base_fakenews_social,
					base_gambling_porn,
					base_gambling_social,
					base_porn_social,
					base_fakenews_gambling_porn,
					base_fakenews_gambling_social,
					base_fakenews_porn_social,
					base_gambling_porn_social,
					base_fakenews_gambling_porn_social]
	for url in hostfiles:
		convert_to_lsrules(url)
		time.sleep(10)
		

def getDirName(url):
	url_segments=url.split('/')
	dir_name='unified_hosts'
	if url_segments[len(url_segments)-2] == 'master':
		dir_name='unified_hosts_base'
		return dir_name
	else:
		dir_name=dir_name+url_segments[url_segments.index('alternates')+1]
		return dir_name

def convert_to_lsrules(target_url):
	output_dir=getDirName(target_url)
	output_script='stevenblack'
	description=''
	name='Steven Black'
	script_number=0
	rule_count=0
	
	#booleans
	description_ends=False
	first_rule=True
	
	#lsrules formatter string and variables
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
	try:
		f_host=urllib2.urlopen(target_url)
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
	except Exception as e:
			print(str(e))

	try:	
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
				else:
					rule_notes='            "notes" : "",\n'
					
			elif (line.startswith('#</') and line.endswith('>')):
				rule_notes='            "notes" : "",\n'
			elif line.startswith('0.0.0.0') and not (line.endswith('0.0.0.0')):
				domain=line.split('0.0.0.0')
				if first_rule:	
					f.write(rule_start)
					first_rule=False
				else :
					f.write(rule_subsequent_start)
				f.write(rule_action)
				rule_creationDate='            "creationDate" : '+str(time.time())+',\n'
				f.write(rule_creationDate)
				rule_modificationDate='            "modificationDate" : '+str(time.time())+',\n'
				f.write(rule_modificationDate)
				f.write(rule_notes)
				f.write(rule_owner)
				f.write(rule_process)
				if '#' in str(domain[1].strip()):
					rule_remote_domain='            "remote-domains" : "'+str(str(domain[1].strip()).split('#')[0])+'"\n'
				else:
					rule_remote_domain='            "remote-domains" : "'+str(domain[1].strip())+'"\n'
				f.write(rule_remote_domain)
				f.write(rule_end)
				rule_count+=1
				if rule_count == 10000:
					print("10,000 rules completed, closing file")
					f.write(end)
					f.close()
					script_number+=1
					rule_count=0
					first_rule=True
					#print("rule-count reset done")
		if rule_count<10000 :				
			f.write(end)
			f.close()
			print(str(rule_count)+' completed, closing the file')
		f_host.close()
		print('conversion completed')
		#quit()
	except Exception as e:
		print(str(e))
if __name__== "__main__":
  main()

