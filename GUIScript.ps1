Write-Host "SSH into your server" -ForegroundColor Green
$servername= Read-Host -Prompt "Enter the servers IP address"
$username= Read-Host -Prompt "Enter your username"
$password= Read-Host -Prompt "Enter your password" -MaskInput

$command = 'df -ah'




<## COMMANDS THAT NEED TO BE RUN THROUGH THE GUI
******************************************************

'cd /mnt/elvinbermycontainer/lab-1/'
'mkdir $Instance'

##########################

'cd /var/log/datadriveblob/'
'mkdir $Instance'
'chown -R freerad:freerad $Instance'


############################
'cd /etc/freeradius/3.0/sites-available/'

'cp -ar merakitemplate $Instance'


'sed -i 's/testsite/$Instance/g' $Instance'

'sed -i 's/99998/$AuthenticationPort/g' $Instance'
'sed -i 's/99999/$AccountingPort/g' $Instance'

'sed -i 's/supersecret/$SharedSecret/g' $Instance'

############################
'cd ../mods-available/'

'nano linelog'
'goto linelog!!!!!'
############################
'cd ../sites-enabled/'

'ln -s ../sites-available/$Instance $Instance'

'chown -R freerad:freerad $Instance'
#>





#Execute SSH command
&(“plink.exe”) -batch -pw $password $username@$servername $command