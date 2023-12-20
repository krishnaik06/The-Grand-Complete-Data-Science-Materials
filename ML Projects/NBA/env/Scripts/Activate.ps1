<#
.Synopsis
Activate a Python virtual environment for the current PowerShell session.

.Description
Pushes the python executable for a virtual environment to the front of the
$Env:PATH environment variable and sets the prompt to signify that you are
in a Python virtual environment. Makes use of the command line switches as
well as the `pyvenv.cfg` file values present in the virtual environment.

.Parameter VenvDir
Path to the directory that contains the virtual environment to activate. The
default value for this is the parent of the directory that the Activate.ps1
script is located within.

.Parameter Prompt
The prompt prefix to display when this virtual environment is activated. By
default, this prompt is the name of the virtual environment folder (VenvDir)
surrounded by parentheses and followed by a single space (ie. '(.venv) ').

.Example
Activate.ps1
Activates the Python virtual environment that contains the Activate.ps1 script.

.Example
Activate.ps1 -Verbose
Activates the Python virtual environment that contains the Activate.ps1 script,
and shows extra information about the activation as it executes.

.Example
Activate.ps1 -VenvDir C:\Users\MyUser\Common\.venv
Activates the Python virtual environment located in the specified location.

.Example
Activate.ps1 -Prompt "MyPython"
Activates the Python virtual environment that contains the Activate.ps1 script,
and prefixes the current prompt with the specified string (surrounded in
parentheses) while the virtual environment is active.

.Notes
On Windows, it may be required to enable this Activate.ps1 script by setting the
execution policy for the user. You can do this by issuing the following PowerShell
command:

PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

For more information on Execution Policies: 
https://go.microsoft.com/fwlink/?LinkID=135170

#>
Param(
    [Parameter(Mandatory = $false)]
    [String]
    $VenvDir,
    [Parameter(Mandatory = $false)]
    [String]
    $Prompt
)

<# Function declarations --------------------------------------------------- #>

<#
.Synopsis
Remove all shell session elements added by the Activate script, including the
addition of the virtual environment's Python executable from the beginning of
the PATH variable.

.Parameter NonDestructive
If present, do not remove this function from the global namespace for the
session.

#>
function global:deactivate ([switch]$NonDestructive) {
    # Revert to original values

    # The prior prompt:
    if (Test-Path -Path Function:_OLD_VIRTUAL_PROMPT) {
        Copy-Item -Path Function:_OLD_VIRTUAL_PROMPT -Destination Function:prompt
        Remove-Item -Path Function:_OLD_VIRTUAL_PROMPT
    }

    # The prior PYTHONHOME:
    if (Test-Path -Path Env:_OLD_VIRTUAL_PYTHONHOME) {
        Copy-Item -Path Env:_OLD_VIRTUAL_PYTHONHOME -Destination Env:PYTHONHOME
        Remove-Item -Path Env:_OLD_VIRTUAL_PYTHONHOME
    }

    # The prior PATH:
    if (Test-Path -Path Env:_OLD_VIRTUAL_PATH) {
        Copy-Item -Path Env:_OLD_VIRTUAL_PATH -Destination Env:PATH
        Remove-Item -Path Env:_OLD_VIRTUAL_PATH
    }

    # Just remove the VIRTUAL_ENV altogether:
    if (Test-Path -Path Env:VIRTUAL_ENV) {
        Remove-Item -Path env:VIRTUAL_ENV
    }

    # Just remove the _PYTHON_VENV_PROMPT_PREFIX altogether:
    if (Get-Variable -Name "_PYTHON_VENV_PROMPT_PREFIX" -ErrorAction SilentlyContinue) {
        Remove-Variable -Name _PYTHON_VENV_PROMPT_PREFIX -Scope Global -Force
    }

    # Leave deactivate function in the global namespace if requested:
    if (-not $NonDestructive) {
        Remove-Item -Path function:deactivate
    }
}

<#
.Description
Get-PyVenvConfig parses the values from the pyvenv.cfg file located in the
given folder, and returns them in a map.

For each line in the pyvenv.cfg file, if that line can be parsed into exactly
two strings separated by `=` (with any amount of whitespace surrounding the =)
then it is considered a `key = value` line. The left hand string is the key,
the right hand is the value.

If the value starts with a `'` or a `"` then the first and last character is
stripped from the value before being captured.

.Parameter ConfigDir
Path to the directory that contains the `pyvenv.cfg` file.
#>
function Get-PyVenvConfig(
    [String]
    $ConfigDir
) {
    Write-Verbose "Given ConfigDir=$ConfigDir, obtain values in pyvenv.cfg"

    # Ensure the file exists, and issue a warning if it doesn't (but still allow the function to continue).
    $pyvenvConfigPath = Join-Path -Resolve -Path $ConfigDir -ChildPath 'pyvenv.cfg' -ErrorAction Continue

    # An empty map will be returned if no config file is found.
    $pyvenvConfig = @{ }

    if ($pyvenvConfigPath) {

        Write-Verbose "File exists, parse `key = value` lines"
        $pyvenvConfigContent = Get-Content -Path $pyvenvConfigPath

        $pyvenvConfigContent | ForEach-Object {
            $keyval = $PSItem -split "\s*=\s*", 2
            if ($keyval[0] -and $keyval[1]) {
                $val = $keyval[1]

                # Remove extraneous quotations around a string value.
                if ("'""".Contains($val.Substring(0, 1))) {
                    $val = $val.Substring(1, $val.Length - 2)
                }

                $pyvenvConfig[$keyval[0]] = $val
                Write-Verbose "Adding Key: '$($keyval[0])'='$val'"
            }
        }
    }
    return $pyvenvConfig
}


<# Begin Activate script --------------------------------------------------- #>

# Determine the containing directory of this script
$VenvExecPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VenvExecDir = Get-Item -Path $VenvExecPath

Write-Verbose "Activation script is located in path: '$VenvExecPath'"
Write-Verbose "VenvExecDir Fullname: '$($VenvExecDir.FullName)"
Write-Verbose "VenvExecDir Name: '$($VenvExecDir.Name)"

# Set values required in priority: CmdLine, ConfigFile, Default
# First, get the location of the virtual environment, it might not be
# VenvExecDir if specified on the command line.
if ($VenvDir) {
    Write-Verbose "VenvDir given as parameter, using '$VenvDir' to determine values"
}
else {
    Write-Verbose "VenvDir not given as a parameter, using parent directory name as VenvDir."
    $VenvDir = $VenvExecDir.Parent.FullName.TrimEnd("\\/")
    Write-Verbose "VenvDir=$VenvDir"
}

# Next, read the `pyvenv.cfg` file to determine any required value such
# as `prompt`.
$pyvenvCfg = Get-PyVenvConfig -ConfigDir $VenvDir

# Next, set the prompt from the command line, or the config file, or
# just use the name of the virtual environment folder.
if ($Prompt) {
    Write-Verbose "Prompt specified as argument, using '$Prompt'"
}
else {
    Write-Verbose "Prompt not specified as argument to script, checking pyvenv.cfg value"
    if ($pyvenvCfg -and $pyvenvCfg['prompt']) {
        Write-Verbose "  Setting based on value in pyvenv.cfg='$($pyvenvCfg['prompt'])'"
        $Prompt = $pyvenvCfg['prompt'];
    }
    else {
        Write-Verbose "  Setting prompt based on parent's directory's name. (Is the directory name passed to venv module when creating the virtual environment)"
        Write-Verbose "  Got leaf-name of $VenvDir='$(Split-Path -Path $venvDir -Leaf)'"
        $Prompt = Split-Path -Path $venvDir -Leaf
    }
}

Write-Verbose "Prompt = '$Prompt'"
Write-Verbose "VenvDir='$VenvDir'"

# Deactivate any currently active virtual environment, but leave the
# deactivate function in place.
deactivate -nondestructive

# Now set the environment variable VIRTUAL_ENV, used by many tools to determine
# that there is an activated venv.
$env:VIRTUAL_ENV = $VenvDir

if (-not $Env:VIRTUAL_ENV_DISABLE_PROMPT) {

    Write-Verbose "Setting prompt to '$Prompt'"

    # Set the prompt to include the env name
    # Make sure _OLD_VIRTUAL_PROMPT is global
    function global:_OLD_VIRTUAL_PROMPT { "" }
    Copy-Item -Path function:prompt -Destination function:_OLD_VIRTUAL_PROMPT
    New-Variable -Name _PYTHON_VENV_PROMPT_PREFIX -Description "Python virtual environment prompt prefix" -Scope Global -Option ReadOnly -Visibility Public -Value $Prompt

    function global:prompt {
        Write-Host -NoNewline -ForegroundColor Green "($_PYTHON_VENV_PROMPT_PREFIX) "
        _OLD_VIRTUAL_PROMPT
    }
}

# Clear PYTHONHOME
if (Test-Path -Path Env:PYTHONHOME) {
    Copy-Item -Path Env:PYTHONHOME -Destination Env:_OLD_VIRTUAL_PYTHONHOME
    Remove-Item -Path Env:PYTHONHOME
}

# Add the venv to the PATH
Copy-Item -Path Env:PATH -Destination Env:_OLD_VIRTUAL_PATH
$Env:PATH = "$VenvExecDir$([System.IO.Path]::PathSeparator)$Env:PATH"

# SIG # Begin signature block
# MIIfoAYJKoZIhvcNAQcCoIIfkTCCH40CAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQH8w7YFlLCE63JNLG
# KX7zUQIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCD50itNqbOCCDp6
# 9ZnhKce5X7vV6KL67iKMbGTUZ4nf36CCDi8wggawMIIEmKADAgECAhAIrUCyYNKc
# TJ9ezam9k67ZMA0GCSqGSIb3DQEBDAUAMGIxCzAJBgNVBAYTAlVTMRUwEwYDVQQK
# EwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5jb20xITAfBgNV
# BAMTGERpZ2lDZXJ0IFRydXN0ZWQgUm9vdCBHNDAeFw0yMTA0MjkwMDAwMDBaFw0z
# NjA0MjgyMzU5NTlaMGkxCzAJBgNVBAYTAlVTMRcwFQYDVQQKEw5EaWdpQ2VydCwg
# SW5jLjFBMD8GA1UEAxM4RGlnaUNlcnQgVHJ1c3RlZCBHNCBDb2RlIFNpZ25pbmcg
# UlNBNDA5NiBTSEEzODQgMjAyMSBDQTEwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAw
# ggIKAoICAQDVtC9C0CiteLdd1TlZG7GIQvUzjOs9gZdwxbvEhSYwn6SOaNhc9es0
# JAfhS0/TeEP0F9ce2vnS1WcaUk8OoVf8iJnBkcyBAz5NcCRks43iCH00fUyAVxJr
# Q5qZ8sU7H/Lvy0daE6ZMswEgJfMQ04uy+wjwiuCdCcBlp/qYgEk1hz1RGeiQIXhF
# LqGfLOEYwhrMxe6TSXBCMo/7xuoc82VokaJNTIIRSFJo3hC9FFdd6BgTZcV/sk+F
# LEikVoQ11vkunKoAFdE3/hoGlMJ8yOobMubKwvSnowMOdKWvObarYBLj6Na59zHh
# 3K3kGKDYwSNHR7OhD26jq22YBoMbt2pnLdK9RBqSEIGPsDsJ18ebMlrC/2pgVItJ
# wZPt4bRc4G/rJvmM1bL5OBDm6s6R9b7T+2+TYTRcvJNFKIM2KmYoX7BzzosmJQay
# g9Rc9hUZTO1i4F4z8ujo7AqnsAMrkbI2eb73rQgedaZlzLvjSFDzd5Ea/ttQokbI
# YViY9XwCFjyDKK05huzUtw1T0PhH5nUwjewwk3YUpltLXXRhTT8SkXbev1jLchAp
# QfDVxW0mdmgRQRNYmtwmKwH0iU1Z23jPgUo+QEdfyYFQc4UQIyFZYIpkVMHMIRro
# OBl8ZhzNeDhFMJlP/2NPTLuqDQhTQXxYPUez+rbsjDIJAsxsPAxWEQIDAQABo4IB
# WTCCAVUwEgYDVR0TAQH/BAgwBgEB/wIBADAdBgNVHQ4EFgQUaDfg67Y7+F8Rhvv+
# YXsIiGX0TkIwHwYDVR0jBBgwFoAU7NfjgtJxXWRM3y5nP+e6mK4cD08wDgYDVR0P
# AQH/BAQDAgGGMBMGA1UdJQQMMAoGCCsGAQUFBwMDMHcGCCsGAQUFBwEBBGswaTAk
# BggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29tMEEGCCsGAQUFBzAC
# hjVodHRwOi8vY2FjZXJ0cy5kaWdpY2VydC5jb20vRGlnaUNlcnRUcnVzdGVkUm9v
# dEc0LmNydDBDBgNVHR8EPDA6MDigNqA0hjJodHRwOi8vY3JsMy5kaWdpY2VydC5j
# b20vRGlnaUNlcnRUcnVzdGVkUm9vdEc0LmNybDAcBgNVHSAEFTATMAcGBWeBDAED
# MAgGBmeBDAEEATANBgkqhkiG9w0BAQwFAAOCAgEAOiNEPY0Idu6PvDqZ01bgAhql
# +Eg08yy25nRm95RysQDKr2wwJxMSnpBEn0v9nqN8JtU3vDpdSG2V1T9J9Ce7FoFF
# UP2cvbaF4HZ+N3HLIvdaqpDP9ZNq4+sg0dVQeYiaiorBtr2hSBh+3NiAGhEZGM1h
# mYFW9snjdufE5BtfQ/g+lP92OT2e1JnPSt0o618moZVYSNUa/tcnP/2Q0XaG3Ryw
# YFzzDaju4ImhvTnhOE7abrs2nfvlIVNaw8rpavGiPttDuDPITzgUkpn13c5Ubdld
# AhQfQDN8A+KVssIhdXNSy0bYxDQcoqVLjc1vdjcshT8azibpGL6QB7BDf5WIIIJw
# 8MzK7/0pNVwfiThV9zeKiwmhywvpMRr/LhlcOXHhvpynCgbWJme3kuZOX956rEnP
# LqR0kq3bPKSchh/jwVYbKyP/j7XqiHtwa+aguv06P0WmxOgWkVKLQcBIhEuWTatE
# QOON8BUozu3xGFYHKi8QxAwIZDwzj64ojDzLj4gLDb879M4ee47vtevLt/B3E+bn
# KD+sEq6lLyJsQfmCXBVmzGwOysWGw/YmMwwHS6DTBwJqakAwSEs0qFEgu60bhQji
# WQ1tygVQK+pKHJ6l/aCnHwZ05/LWUpD9r4VIIflXO7ScA+2GRfS0YW6/aOImYIbq
# yK+p/pQd52MbOoZWeE4wggd3MIIFX6ADAgECAhAHHxQbizANJfMU6yMM0NHdMA0G
# CSqGSIb3DQEBCwUAMGkxCzAJBgNVBAYTAlVTMRcwFQYDVQQKEw5EaWdpQ2VydCwg
# SW5jLjFBMD8GA1UEAxM4RGlnaUNlcnQgVHJ1c3RlZCBHNCBDb2RlIFNpZ25pbmcg
# UlNBNDA5NiBTSEEzODQgMjAyMSBDQTEwHhcNMjIwMTE3MDAwMDAwWhcNMjUwMTE1
# MjM1OTU5WjB8MQswCQYDVQQGEwJVUzEPMA0GA1UECBMGT3JlZ29uMRIwEAYDVQQH
# EwlCZWF2ZXJ0b24xIzAhBgNVBAoTGlB5dGhvbiBTb2Z0d2FyZSBGb3VuZGF0aW9u
# MSMwIQYDVQQDExpQeXRob24gU29mdHdhcmUgRm91bmRhdGlvbjCCAiIwDQYJKoZI
# hvcNAQEBBQADggIPADCCAgoCggIBAKgc0BTT+iKbtK6f2mr9pNMUTcAJxKdsuOiS
# YgDFfwhjQy89koM7uP+QV/gwx8MzEt3c9tLJvDccVWQ8H7mVsk/K+X+IufBLCgUi
# 0GGAZUegEAeRlSXxxhYScr818ma8EvGIZdiSOhqjYc4KnfgfIS4RLtZSrDFG2tN1
# 6yS8skFa3IHyvWdbD9PvZ4iYNAS4pjYDRjT/9uzPZ4Pan+53xZIcDgjiTwOh8VGu
# ppxcia6a7xCyKoOAGjvCyQsj5223v1/Ig7Dp9mGI+nh1E3IwmyTIIuVHyK6Lqu35
# 2diDY+iCMpk9ZanmSjmB+GMVs+H/gOiofjjtf6oz0ki3rb7sQ8fTnonIL9dyGTJ0
# ZFYKeb6BLA66d2GALwxZhLe5WH4Np9HcyXHACkppsE6ynYjTOd7+jN1PRJahN1oE
# RzTzEiV6nCO1M3U1HbPTGyq52IMFSBM2/07WTJSbOeXjvYR7aUxK9/ZkJiacl2iZ
# I7IWe7JKhHohqKuceQNyOzxTakLcRkzynvIrk33R9YVqtB4L6wtFxhUjvDnQg16x
# ot2KVPdfyPAWd81wtZADmrUtsZ9qG79x1hBdyOl4vUtVPECuyhCxaw+faVjumapP
# Unwo8ygflJJ74J+BYxf6UuD7m8yzsfXWkdv52DjL74TxzuFTLHPyARWCSCAbzn3Z
# Ily+qIqDAgMBAAGjggIGMIICAjAfBgNVHSMEGDAWgBRoN+Drtjv4XxGG+/5hewiI
# ZfROQjAdBgNVHQ4EFgQUt/1Teh2XDuUj2WW3siYWJgkZHA8wDgYDVR0PAQH/BAQD
# AgeAMBMGA1UdJQQMMAoGCCsGAQUFBwMDMIG1BgNVHR8Ega0wgaowU6BRoE+GTWh0
# dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydFRydXN0ZWRHNENvZGVTaWdu
# aW5nUlNBNDA5NlNIQTM4NDIwMjFDQTEuY3JsMFOgUaBPhk1odHRwOi8vY3JsNC5k
# aWdpY2VydC5jb20vRGlnaUNlcnRUcnVzdGVkRzRDb2RlU2lnbmluZ1JTQTQwOTZT
# SEEzODQyMDIxQ0ExLmNybDA+BgNVHSAENzA1MDMGBmeBDAEEATApMCcGCCsGAQUF
# BwIBFhtodHRwOi8vd3d3LmRpZ2ljZXJ0LmNvbS9DUFMwgZQGCCsGAQUFBwEBBIGH
# MIGEMCQGCCsGAQUFBzABhhhodHRwOi8vb2NzcC5kaWdpY2VydC5jb20wXAYIKwYB
# BQUHMAKGUGh0dHA6Ly9jYWNlcnRzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydFRydXN0
# ZWRHNENvZGVTaWduaW5nUlNBNDA5NlNIQTM4NDIwMjFDQTEuY3J0MAwGA1UdEwEB
# /wQCMAAwDQYJKoZIhvcNAQELBQADggIBABxv4AeV/5ltkELHSC63fXAFYS5tadcW
# TiNc2rskrNLrfH1Ns0vgSZFoQxYBFKI159E8oQQ1SKbTEubZ/B9kmHPhprHya08+
# VVzxC88pOEvz68nA82oEM09584aILqYmj8Pj7h/kmZNzuEL7WiwFa/U1hX+XiWfL
# IJQsAHBla0i7QRF2de8/VSF0XXFa2kBQ6aiTsiLyKPNbaNtbcucaUdn6vVUS5izW
# OXM95BSkFSKdE45Oq3FForNJXjBvSCpwcP36WklaHL+aHu1upIhCTUkzTHMh8b86
# WmjRUqbrnvdyR2ydI5l1OqcMBjkpPpIV6wcc+KY/RH2xvVuuoHjlUjwq2bHiNoX+
# W1scCpnA8YTs2d50jDHUgwUo+ciwpffH0Riq132NFmrH3r67VaN3TuBxjI8SIZM5
# 8WEDkbeoriDk3hxU8ZWV7b8AW6oyVBGfM06UgkfMb58h+tJPrFx8VI/WLq1dTqMf
# ZOm5cuclMnUHs2uqrRNtnV8UfidPBL4ZHkTcClQbCoz0UbLhkiDvIS00Dn+BBcxw
# /TKqVL4Oaz3bkMSsM46LciTeucHY9ExRVt3zy7i149sd+F4QozPqn7FrSVHXmem3
# r7bjyHTxOgqxRCVa18Vtx7P/8bYSBeS+WHCKcliFCecspusCDSlnRUjZwyPdP0VH
# xaZg2unjHY3rMYIQxzCCEMMCAQEwfTBpMQswCQYDVQQGEwJVUzEXMBUGA1UEChMO
# RGlnaUNlcnQsIEluYy4xQTA/BgNVBAMTOERpZ2lDZXJ0IFRydXN0ZWQgRzQgQ29k
# ZSBTaWduaW5nIFJTQTQwOTYgU0hBMzg0IDIwMjEgQ0ExAhAHHxQbizANJfMU6yMM
# 0NHdMA0GCWCGSAFlAwQCAQUAoIGaMBkGCSqGSIb3DQEJAzEMBgorBgEEAYI3AgEE
# MBwGCisGAQQBgjcCAQsxDjAMBgorBgEEAYI3AgEVMC4GCisGAQQBgjcCAQwxIDAe
# oByAGgBQAHkAdABoAG8AbgAgADMALgA5AC4AMQAwMC8GCSqGSIb3DQEJBDEiBCBW
# STMEpY5oTqEtnhE8rXHTfUpY7MZMEfDbBKbS1J0cLTANBgkqhkiG9w0BAQEFAASC
# AgAPzlwbodN8MHW8YdekShG0qP3JBHOiS/34BAZDjSlF+zFgZ0mj7Ve1M5jh2rwX
# etpEDZVtibeDX5E844JWk696lLd6/I+W1z/lXChrg4LLZvAs5KyBbrsfTlvMmEDJ
# onhCKNodHk/11vWbvZKHFOl/1DrkTPi02FLlgvG9APGRy6bRHEjSntv7vbxHIdmO
# 6n4sY3Kr370PPkS1tsvVikuiyB5xHb3Hp7t2b9vu1ljgUuljP0ZPdAJQrBRaY5Fx
# ur20lxJRhzfw0ZERQpv5ckNWN772yIE9oN4F/fQdXiJr93yC/obbOS4DHT+6fDQI
# uvu07XEUVABBI+ZFYT96BTkAK+J9aC3Ego8SkUZG3OVuLzm46ZxtUrOW9udwIsKk
# eo8/swB0KTqPS7wPh6S48dzeOMtLLwy7CdoV8g7zICSlpZCtATAFzbezGJIMAkD0
# 5z2sC4Sh0w2L/YdyCJYCHx8x9zvWflz7mwzQaMkcjf6tDlASzB2CHzHGqvTxG3pS
# 45VNz+AqMqc/8qOYkj5RBALjwqYZgkhnJV3kjo8RhLXtC17/XWK7uG9GRG9iSgKk
# vjD4ZZSzXqqxjMowHst8nX40Qk9vgcDCwt+A+5/p/leMEz6Ke/Dda18cUcnQJ2vi
# gdt9tEw3eyOJfi4YEATe/OebdvuLMbkBStDjoXUUfk94g6GCDX4wgg16BgorBgEE
# AYI3AwMBMYINajCCDWYGCSqGSIb3DQEHAqCCDVcwgg1TAgEDMQ8wDQYJYIZIAWUD
# BAIBBQAweAYLKoZIhvcNAQkQAQSgaQRnMGUCAQEGCWCGSAGG/WwHATAxMA0GCWCG
# SAFlAwQCAQUABCBgohShZG6GGnEC2VNFzpMj8SFLZ+uwOrVJR9x1nrutHAIRAM01
# q7AObTeGY7SVhi6kp7AYDzIwMjIwMTE3MTUyOTE3WqCCCjcwggT+MIID5qADAgEC
# AhANQkrgvjqI/2BAIc4UAPDdMA0GCSqGSIb3DQEBCwUAMHIxCzAJBgNVBAYTAlVT
# MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
# b20xMTAvBgNVBAMTKERpZ2lDZXJ0IFNIQTIgQXNzdXJlZCBJRCBUaW1lc3RhbXBp
# bmcgQ0EwHhcNMjEwMTAxMDAwMDAwWhcNMzEwMTA2MDAwMDAwWjBIMQswCQYDVQQG
# EwJVUzEXMBUGA1UEChMORGlnaUNlcnQsIEluYy4xIDAeBgNVBAMTF0RpZ2lDZXJ0
# IFRpbWVzdGFtcCAyMDIxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
# wuZhhGfFivUNCKRFymNrUdc6EUK9CnV1TZS0DFC1JhD+HchvkWsMlucaXEjvROW/
# m2HNFZFiWrj/ZwucY/02aoH6KfjdK3CF3gIY83htvH35x20JPb5qdofpir34hF0e
# dsnkxnZ2OlPR0dNaNo/Go+EvGzq3YdZz7E5tM4p8XUUtS7FQ5kE6N1aG3JMjjfdQ
# Jehk5t3Tjy9XtYcg6w6OLNUj2vRNeEbjA4MxKUpcDDGKSoyIxfcwWvkUrxVfbENJ
# Cf0mI1P2jWPoGqtbsR0wwptpgrTb/FZUvB+hh6u+elsKIC9LCcmVp42y+tZji06l
# chzun3oBc/gZ1v4NSYS9AQIDAQABo4IBuDCCAbQwDgYDVR0PAQH/BAQDAgeAMAwG
# A1UdEwEB/wQCMAAwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwQQYDVR0gBDowODA2
# BglghkgBhv1sBwEwKTAnBggrBgEFBQcCARYbaHR0cDovL3d3dy5kaWdpY2VydC5j
# b20vQ1BTMB8GA1UdIwQYMBaAFPS24SAd/imu0uRhpbKiJbLIFzVuMB0GA1UdDgQW
# BBQ2RIaOpLqwZr68KC0dRDbd42p6vDBxBgNVHR8EajBoMDKgMKAuhixodHRwOi8v
# Y3JsMy5kaWdpY2VydC5jb20vc2hhMi1hc3N1cmVkLXRzLmNybDAyoDCgLoYsaHR0
# cDovL2NybDQuZGlnaWNlcnQuY29tL3NoYTItYXNzdXJlZC10cy5jcmwwgYUGCCsG
# AQUFBwEBBHkwdzAkBggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29t
# ME8GCCsGAQUFBzAChkNodHRwOi8vY2FjZXJ0cy5kaWdpY2VydC5jb20vRGlnaUNl
# cnRTSEEyQXNzdXJlZElEVGltZXN0YW1waW5nQ0EuY3J0MA0GCSqGSIb3DQEBCwUA
# A4IBAQBIHNy16ZojvOca5yAOjmdG/UJyUXQKI0ejq5LSJcRwWb4UoOUngaVNFBUZ
# B3nw0QTDhtk7vf5EAmZN7WmkD/a4cM9i6PVRSnh5Nnont/PnUp+Tp+1DnnvntN1B
# Ion7h6JGA0789P63ZHdjXyNSaYOC+hpT7ZDMjaEXcw3082U5cEvznNZ6e9oMvD0y
# 0BvL9WH8dQgAdryBDvjA4VzPxBFy5xtkSdgimnUVQvUtMjiB2vRgorq0Uvtc4GEk
# JU+y38kpqHNDUdq9Y9YfW5v3LhtPEx33Sg1xfpe39D+E68Hjo0mh+s6nv1bPull2
# YYlffqe0jmd4+TaY4cso2luHpoovMIIFMTCCBBmgAwIBAgIQCqEl1tYyG35B5AXa
# NpfCFTANBgkqhkiG9w0BAQsFADBlMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGln
# aUNlcnQgSW5jMRkwFwYDVQQLExB3d3cuZGlnaWNlcnQuY29tMSQwIgYDVQQDExtE
# aWdpQ2VydCBBc3N1cmVkIElEIFJvb3QgQ0EwHhcNMTYwMTA3MTIwMDAwWhcNMzEw
# MTA3MTIwMDAwWjByMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5j
# MRkwFwYDVQQLExB3d3cuZGlnaWNlcnQuY29tMTEwLwYDVQQDEyhEaWdpQ2VydCBT
# SEEyIEFzc3VyZWQgSUQgVGltZXN0YW1waW5nIENBMIIBIjANBgkqhkiG9w0BAQEF
# AAOCAQ8AMIIBCgKCAQEAvdAy7kvNj3/dqbqCmcU5VChXtiNKxA4HRTNREH3Q+X1N
# aH7ntqD0jbOI5Je/YyGQmL8TvFfTw+F+CNZqFAA49y4eO+7MpvYyWf5fZT/gm+vj
# RkcGGlV+Cyd+wKL1oODeIj8O/36V+/OjuiI+GKwR5PCZA207hXwJ0+5dyJoLVOOo
# CXFr4M8iEA91z3FyTgqt30A6XLdR4aF5FMZNJCMwXbzsPGBqrC8HzP3w6kfZiFBe
# /WZuVmEnKYmEUeaC50ZQ/ZQqLKfkdT66mA+Ef58xFNat1fJky3seBdCEGXIX8RcG
# 7z3N1k3vBkL9olMqT4UdxB08r8/arBD13ays6Vb/kwIDAQABo4IBzjCCAcowHQYD
# VR0OBBYEFPS24SAd/imu0uRhpbKiJbLIFzVuMB8GA1UdIwQYMBaAFEXroq/0ksuC
# MS1Ri6enIZ3zbcgPMBIGA1UdEwEB/wQIMAYBAf8CAQAwDgYDVR0PAQH/BAQDAgGG
# MBMGA1UdJQQMMAoGCCsGAQUFBwMIMHkGCCsGAQUFBwEBBG0wazAkBggrBgEFBQcw
# AYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29tMEMGCCsGAQUFBzAChjdodHRwOi8v
# Y2FjZXJ0cy5kaWdpY2VydC5jb20vRGlnaUNlcnRBc3N1cmVkSURSb290Q0EuY3J0
# MIGBBgNVHR8EejB4MDqgOKA2hjRodHRwOi8vY3JsNC5kaWdpY2VydC5jb20vRGln
# aUNlcnRBc3N1cmVkSURSb290Q0EuY3JsMDqgOKA2hjRodHRwOi8vY3JsMy5kaWdp
# Y2VydC5jb20vRGlnaUNlcnRBc3N1cmVkSURSb290Q0EuY3JsMFAGA1UdIARJMEcw
# OAYKYIZIAYb9bAACBDAqMCgGCCsGAQUFBwIBFhxodHRwczovL3d3dy5kaWdpY2Vy
# dC5jb20vQ1BTMAsGCWCGSAGG/WwHATANBgkqhkiG9w0BAQsFAAOCAQEAcZUS6VGH
# VmnN793afKpjerN4zwY3QITvS4S/ys8DAv3Fp8MOIEIsr3fzKx8MIVoqtwU0HWqu
# mfgnoma/Capg33akOpMP+LLR2HwZYuhegiUexLoceywh4tZbLBQ1QwRostt1AuBy
# x5jWPGTlH0gQGF+JOGFNYkYkh2OMkVIsrymJ5Xgf1gsUpYDXEkdws3XVk4WTfraS
# Z/tTYYmo9WuWwPRYaQ18yAGxuSh1t5ljhSKMYcp5lH5Z/IwP42+1ASa2bKXuh1Eh
# 5Fhgm7oMLSttosR+u8QlK0cCCHxJrhO24XxCQijGGFbPQTS2Zl22dHv1VjMiLyI2
# skuiSpXY9aaOUjGCAoYwggKCAgEBMIGGMHIxCzAJBgNVBAYTAlVTMRUwEwYDVQQK
# EwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5jb20xMTAvBgNV
# BAMTKERpZ2lDZXJ0IFNIQTIgQXNzdXJlZCBJRCBUaW1lc3RhbXBpbmcgQ0ECEA1C
# SuC+Ooj/YEAhzhQA8N0wDQYJYIZIAWUDBAIBBQCggdEwGgYJKoZIhvcNAQkDMQ0G
# CyqGSIb3DQEJEAEEMBwGCSqGSIb3DQEJBTEPFw0yMjAxMTcxNTI5MTdaMCsGCyqG
# SIb3DQEJEAIMMRwwGjAYMBYEFOHXgqjhkb7va8oWkbWqtJSmJJvzMC8GCSqGSIb3
# DQEJBDEiBCDtBHQ+tXcL8vDjT0OquW5811EitOjdQ5cZZkefXLoOCjA3BgsqhkiG
# 9w0BCRACLzEoMCYwJDAiBCCzEJAGvArZgweRVyngRANBXIPjKSthTyaWTI01cez1
# qTANBgkqhkiG9w0BAQEFAASCAQC9Dapy/eTCob+N7zNLMJMw4UVb6+eV3WuS7Xy3
# cCo8YtpstK4msBBqvTgt31POIRIELa4SgN5Lgl91IyhrxZS0EGmnH23Dh5FNFh/Q
# PKcIe6F0NGA2xEaIbPgHe384AHPSbtl87dxtFtpfbPxkttw5OlF7kdbNmCgvZL9d
# Ji+xckrCjV8qGdDwDjjRi65beUHCvk6yKvM+6uwCipZ15EAeVmxIbb/5ZwYeYsg1
# os6RakuNVPNOx80IR0JYum+I5U+6lpYtsGFnRCFyh3Abd6OU+Mkyj7Q40R9Qq/ka
# +gCrmLJB6IF2aewXTKWlLstCevIsOSsZwEKIhAN6T7jUHDz4
# SIG # End signature block
