# .NET Framework classes
Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms

# XAML
[xml]$XAML = @"
<Window x:Class="MYTHIRDTest.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="clr-namespace:MYTHIRDTest"
        mc:Ignorable="d"
        Title="MainWindow" Height="450" Width="800">

    <Grid RenderTransformOrigin="0.465,0.502">

        <Label x:Name="IPaddress"
        Content="IP Address:" 
        HorizontalAlignment="Left" Height="40" Margin="78,106,0,0" VerticalAlignment="Top" Width="134" 
        Foreground="#FF2277C1" FontFamily="Century Gothic" FontSize="22" Background="Transparent"
        />

        <Label x:Name="Username"
        Content="Username:" 
        HorizontalAlignment="Left" Height="40" Margin="78,159,0,0" VerticalAlignment="Top" Width="134" 
        Foreground="#FF070606" FontFamily="Century Gothic" FontSize="22"
        />

        <Label x:Name="Password"
        Content="Password:" 
        HorizontalAlignment="Left" Height="40" Margin="78,199,0,0" VerticalAlignment="Top" Width="134" 
        FontFamily="Century Gothic" FontSize="22"
        />

        <PasswordBox x:Name="inputPassword"
        HorizontalAlignment="Left" Margin="245,201,0,0" VerticalAlignment="Top" Width="259" 
        Password="" Height="32" FontSize="18" BorderBrush="Black"
        />

        <TextBox x:Name="inputIPaddress"
        HorizontalAlignment="Left" Margin="245,110,0,0" TextWrapping="Wrap" VerticalAlignment="Top" Width="259" Height="32" 
        BorderBrush="#FF060607" FontSize="18"
        />

        <TextBox x:Name="inputUsername"
        HorizontalAlignment="Left" Margin="245,159,0,0" TextWrapping="Wrap" VerticalAlignment="Top" Width="259" Height="32" 
        BorderBrush="#FF060607" FontSize="18"
        />

        <Button x:Name="submit"
        Content="OK" 
        HorizontalAlignment="Left" Margin="477,284,0,0" VerticalAlignment="Top" Height="34" Width="135" 
        Background="#FF5CBC66" FontFamily="Bahnschrift SemiLight" FontSize="22"
        />

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
$submit = $MainWindow.FindName('submit')
$inputPassword = $MainWindow.FindName('inputPassword')
$inputUsername = $MainWindow.FindName('inputUsername')
$inputIPaddress = $MainWindow.FindName('inputIPaddress')

#adds functionality to the submit button
$submit.Add_Click({
    $MainWindow.hide()  #closes the GUI window

    #saves inputted values from textboxes to variables
    $script:password = $inputPassword.Password.ToString()
    $script:servername= $inputIPaddress.Text.ToString()
    $script:username = $inputUsername.Text.ToString()
})

# Show MainWindow
$MainWindow.ShowDialog() | Out-Null

$command = 'df -ah'

#if the ssh is successful run the CommandGUI script to open the next GUI window
#else execute the ErrorSSH script 
if (&(“plink.exe") -batch -pw $password $username@$servername $command){
    $script = $PSScriptRoot+"\CommandGUI.ps1"
    . $script
}
else {
    $script = $PSScriptRoot+"\ErrorSSH.ps1"
    . $script
}


