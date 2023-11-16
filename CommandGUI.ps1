# .NET Framework classes
Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms

# XAML
[xml]$XAML = @"
<Window x:Name="Window2" x:Class="MYTHIRDTest.Window1"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="clr-namespace:MYTHIRDTest"
        mc:Ignorable="d"
        Title="New Radius Instance" Height="450" Width="800">
    <Grid Background="#FFD7E6FC">
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="4*"/>
            <ColumnDefinition Width="3*"/>
            <ColumnDefinition Width="153*"/>
        </Grid.ColumnDefinitions>

        <Label x:Name="RadiusInstanceName" 
        Content="Radius Instance Name:" 
        HorizontalAlignment="Left" Margin="23,59,0,0" VerticalAlignment="Top" Grid.Column="2" FontWeight="Bold" FontFamily="Bahnschrift SemiBold" FontSize="16"/>
        
        <Label x:Name="UDPports" 
        Content="Enter UDP Ports" 
        HorizontalAlignment="Left" Height="32" Margin="23,132,0,0" VerticalAlignment="Top" Width="130" Grid.Column="2" FontWeight="Bold" FontSize="16" FontFamily="Bahnschrift SemiBold"/>
        
        <Label x:Name="AuthenticationPort" 
        Content="Authentication Port: " 
        HorizontalAlignment="Left" Height="29" Margin="75,169,0,0" VerticalAlignment="Top" Width="128" Grid.Column="2" FontFamily="Bahnschrift SemiBold" FontSize="13"/>
        
        <Label x:Name="AccountingPort" 
        Content="Accounting Port:" 
        HorizontalAlignment="Left" Height="29" Margin="77,216,0,0" VerticalAlignment="Top" Width="108" Grid.Column="2" FontFamily="Bahnschrift SemiBold" FontSize="13"/>
        
        <Label x:Name="SharedSecret" 
        Content="Radius Shared Secret:" 
        HorizontalAlignment="Left" Height="32" Margin="31,288,0,0" VerticalAlignment="Top" Width="186" Grid.Column="2" FontFamily="Bahnschrift SemiBold" FontSize="16"/>
        
        <Button x:Name="Submit" 
        Content="Submit" 
        HorizontalAlignment="Left" Height="30" Margin="566,330,0,0" VerticalAlignment="Top" Width="136" Grid.Column="2" FontFamily="Bahnschrift SemiBold" FontSize="18" Background="#FF4FE247"/>
        
        <TextBox x:Name="inputInstance" 
        Grid.Column="2" HorizontalAlignment="Left" Height="29" Margin="211,59,0,0" TextWrapping="Wrap" VerticalAlignment="Top" Width="220" FontSize="16" FontFamily="Bahnschrift SemiBold"/>
        
        <TextBox x:Name="inputAuthenticationPort" 
        Grid.Column="2" HorizontalAlignment="Left" Height="29" Margin="211,169,0,0" TextWrapping="Wrap" VerticalAlignment="Top" Width="219" FontFamily="Bahnschrift SemiBold" FontSize="13"/>
        
        <TextBox x:Name="inputAccountingPort" 
        Grid.Column="2" HorizontalAlignment="Left" Height="29" Margin="211,217,0,0" TextWrapping="Wrap" VerticalAlignment="Top" Width="219" FontFamily="Bahnschrift SemiBold" FontSize="13"/>
        
        <PasswordBox x:Name="inputSharedSecret" 
        Grid.Column="2" HorizontalAlignment="Left" Height="28" Margin="211,288,0,0" VerticalAlignment="Top" Width="219" FontFamily="Bahnschrift SemiBold" FontSize="16"/>

    </Grid>
</Window>

"@

#Allows powershell to read XAML
$XAML.Window.RemoveAttribute('x:Class')
$XAML.Window.RemoveAttribute('mc:Ignorable')
$XAMLReader = New-Object System.Xml.XmlNodeReader $XAML
$MainWindow = [Windows.Markup.XamlReader]::Load($XAMLReader)

# UI Elements
$XAML.SelectNodes("//*[@Name]") | ForEach-Object{Set-Variable -Name ($_.Name) -Value $MainWindow.FindName($_.Name)}
$inputInstance = $MainWindow.FindName('inputInstance')
$inputAccountingPort = $MainWindow.FindName('inputAccountingPort')
$inputAuthenticationPort = $MainWindow.FindName('inputAuthenticationPort')
$inputSharedSecret = $MainWindow.FindName('inputSharedSecret')
$Submit = $MainWindow.FindName('Submit')


#Adds functionality to the submit button
$submit.Add_Click({
    $MainWindow.Hide()  #closes GUI window

    #saves inputted values from textboxes to variables
    $script:Instance = $inputInstance.Text.ToString()   
    $script:AccountingPort= $inputAccountingPort.Text.ToString()
    $script:AuthenticationPort = $inputAuthenticationPort.Text.ToString()
    $script:SharedSecret = $inputSharedSecret.Password.ToString()

})


# Show MainWindow
$MainWindow.ShowDialog() | Out-Null
 
#SSH into server and runs series of commands
&(“plink.exe") -batch -pw $password $username@$servername "cd /home/customers/; sudo mkdir $Instance; cd /var/log/datadriveblob/; sudo mkdir $Instance; sudo chown -R freerad:freerad $Instance; cd /etc/freeradius/sites-available/; cp -ar merakitemplate $Instance; sed -i 's/testsite/$Instance/g' $Instance; sed -i 's/99998/$AuthenticationPort/g' $Instance; sed -i 's/99999/$AccountingPort/g' $Instance; sed -i 's/supersecret/$SharedSecret/g' $Instance;"


#resets the username, servername, and password for next execution

$username = ""
$servername = ""
$password = ""



