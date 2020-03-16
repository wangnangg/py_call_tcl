proc find_end_sym {buffer} {
    for {set i 0} {$i < [string length $buffer]} {incr i} {
        if [string equal [string index $buffer $i] "\0"] {
            return $i
        }
    }

    return -1
}

proc read_at_most {fin num} {
    fconfigure $fin -blocking 0
    set input [read $fin $num]
    if {[string length $input] == 0} {
        fconfigure $fin -blocking 1
        set input [read $fin 1]
    }
    return $input
}


set current_buffer ""

while {1} {
    set input [read_at_most stdin 256]
    set pos [find_end_sym $input]
    if {$pos == -1} {
        append current_buffer $input
    } else {
        append current_buffer [string range $input 0 [expr {$pos - 1}]]
        set code [catch {eval $current_buffer} result]
        if {$code != 0} {
            puts -nonewline stderr "$result"
        }

        puts -nonewline stdout "\0"
        puts -nonewline stderr "$code\0"
        flush stdout
        flush stderr
        set current_buffer [string range $input [expr {$pos + 1}] [string length $input]]
    }
    if {[eof stdin]} {
        break
    }
}