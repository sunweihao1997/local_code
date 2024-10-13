module your_module
    implicit none
    integer :: n = 2
end module

program main
    implicit none
    real :: x

    block
        use your_module, only: n ! you can import modules within blocks
        real :: y ! local scope variable
        y = 2.0
        x = y ** n
        print *, y
    end block
    ! print *, y ! this is not allowed as y only exists during the block's scope
    print *, x  ! prints 4.00000000
end program