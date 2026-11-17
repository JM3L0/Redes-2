param(
    [Parameter(Position=0)]
    [ValidateSet("lan", "wan_loss", "wan_noloss", "clean")]
    [string]$Mode = "clean"
)

python "$PSScriptRoot\setup_netem.py" $Mode
