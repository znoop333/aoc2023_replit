int fn_px(int x, int m, int a, int s, int total) 
{
if (a < 2006) 
    return fn_qkq(x, m, a, s, total);
if (m > 2090) 
    return total;
return fn_rfg(x, m, a, s, total);
}

int fn_pv(int x, int m, int a, int s, int total) 
{
if (a > 1716) 
    return 0;
return total;
}

int fn_lnx(int x, int m, int a, int s, int total) 
{
if (m > 1548) 
    return total;
return total;
}

int fn_rfg(int x, int m, int a, int s, int total) 
{
if (s < 537) 
    return fn_gd(x, m, a, s, total);
if (x > 2440) 
    return 0;
return total;
}

int fn_qs(int x, int m, int a, int s, int total) 
{
if (s > 3448) 
    return total;
return fn_lnx(x, m, a, s, total);
}

int fn_qkq(int x, int m, int a, int s, int total) 
{
if (x < 1416) 
    return total;
return fn_crn(x, m, a, s, total);
}

int fn_crn(int x, int m, int a, int s, int total) 
{
if (x > 2662) 
    return total;
return 0;
}

int fn_in(int x, int m, int a, int s, int total) 
{
if (s < 1351) 
    return fn_px(x, m, a, s, total);
return fn_qqz(x, m, a, s, total);
}

int fn_qqz(int x, int m, int a, int s, int total) 
{
if (s > 2770) 
    return fn_qs(x, m, a, s, total);
if (m < 1801) 
    return fn_hdj(x, m, a, s, total);
return 0;
}

int fn_gd(int x, int m, int a, int s, int total) 
{
if (a > 3333) 
    return 0;
return 0;
}

int fn_hdj(int x, int m, int a, int s, int total) 
{
if (m > 838) 
    return total;
return fn_pv(x, m, a, s, total);
}

int main(void) {
int total = 0;
    total += fn_in(787, 2655, 1222, 2876, 7540);
    total += fn_in(1679, 44, 2067, 496, 4286);
    total += fn_in(2036, 264, 79, 2244, 4623);
    total += fn_in(2461, 1339, 466, 291, 4557);
    total += fn_in(2127, 1623, 2188, 1013, 6951);
printf("%d", total);
}
