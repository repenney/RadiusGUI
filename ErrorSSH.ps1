# .NET Framework classes
Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName System.Windows.Forms

# XAML
[xml]$XAML = @"
<Window x:Class="MYTHIRDTest.Window2"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="clr-namespace:MYTHIRDTest"
        mc:Ignorable="d"
        Title="Error" Height="176" Width="449" Background="#FFFFFAF9">
    <Grid Margin="10,-12,10,-6">

        <Label  Content="Unable to SSH into server. &#xD;&#xA;Please enter a valid IP address, username, and password combination." HorizontalAlignment="Left" Height="54" Margin="10,35,0,0" VerticalAlignment="Top" Width="397"/>
        
        <Button x:Name="Quit"
        Content="Quit" 
        HorizontalAlignment="Left" Height="22" Margin="72,105,0,0" VerticalAlignment="Top" Width="86" Background="#FFF1533C"/>
        
        <Button x:Name="TryAgain"
        Content="Try Again" 
        HorizontalAlignment="Left" Height="22" Margin="251,105,0,0" VerticalAlignment="Top" Width="86" Background="#FF5BDA09"/>

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
$Quit = $MainWindow.FindName('Quit')
$TryAgain = $MainWindow.FindName('TryAgain')

#adds functionality to the Quit button
$Quit.Add_Click({
    $MainWindow.hide()  #closes the GUI window
})

#adds functionality to the Try Again button
$TryAgain.Add_Click({
    $MainWindow.hide()  #closes the GUI window

    #Executes the SSHGUI script so the user can re-attempt login 
    $script = $PSScriptRoot+"\SSHGUI.ps1"
    . $script
})


# Show MainWindow
$MainWindow.ShowDialog() | Out-Null