open_project ${project_path}

reset_run synth_1
launch_runs impl_1 -to_step write_bitstream -jobs 16
wait_on_run impl_1

write_cfgmem  -format mcs -size 16 -interface SPIx1 -loadbit {up 0x00000000 "${bit_path}" } -file "${mcs_path}"

open_hw_manager
connect_hw_server -allow_non_jtag
open_hw_target

set_property PROGRAM.FILE {${bit_path}} [get_hw_devices ${device}]
current_hw_device [get_hw_devices ${device}]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices ${device}] 0]

create_hw_cfgmem -hw_device [get_hw_devices ${device}] -mem_dev [lindex [get_cfgmem_parts {${memory_device}}] 0]
set_property PROGRAM.ADDRESS_RANGE  {use_file} [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.FILES [list "${mcs_path}" ] [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.UNUSED_PIN_TERMINATION {pull-none} [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.BLANK_CHECK  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.ERASE  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.CFG_PROGRAM  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.VERIFY  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.CHECKSUM  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.ADDRESS_RANGE  {use_file} [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.FILES [list "${mcs_path}" ] [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.PRM_FILE {} [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.UNUSED_PIN_TERMINATION {pull-none} [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.BLANK_CHECK  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.ERASE  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.CFG_PROGRAM  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.VERIFY  1 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
set_property PROGRAM.CHECKSUM  0 [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]

startgroup
create_hw_bitstream -hw_device [lindex [get_hw_devices ${device}] 0] [get_property PROGRAM.HW_CFGMEM_BITFILE [ lindex [get_hw_devices ${device}] 0]]; program_hw_devices [lindex [get_hw_devices ${device}] 0]; refresh_hw_device [lindex [get_hw_devices ${device}] 0];
program_hw_cfgmem -hw_cfgmem [ get_property PROGRAM.HW_CFGMEM [lindex [get_hw_devices ${device}] 0]]
endgroup

close_project
