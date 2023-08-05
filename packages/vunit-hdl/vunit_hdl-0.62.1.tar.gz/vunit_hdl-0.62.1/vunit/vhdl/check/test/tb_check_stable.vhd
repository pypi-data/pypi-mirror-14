-- This test suite verifies the check_stable checker.
--
-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this file,
-- You can obtain one at http://mozilla.org/MPL/2.0/.
--
-- Copyright (c) 2014-2015, Lars Asplund lars.anders.asplund@gmail.com

library ieee;
use ieee.std_logic_1164.all;
library vunit_lib;
use vunit_lib.run_types_pkg.all;
use vunit_lib.run_base_pkg.all;
use vunit_lib.run_pkg.all;
use vunit_lib.log_types_pkg.all;
use vunit_lib.check_types_pkg.all;
use vunit_lib.check_special_types_pkg.all;
use vunit_lib.check_pkg.all;
use work.test_support.all;
use work.test_count.all;

entity tb_check_stable is
  generic (
    runner_cfg : runner_cfg_t := runner_cfg_default);
end entity tb_check_stable;

architecture test_fixture of tb_check_stable is
  signal clk : std_logic := '0';
  signal one : std_logic := '1';
  signal zero : std_logic := '0';

  signal check_stable_in_1, check_stable_in_2, check_stable_in_3 : std_logic_vector(1 to 5) := "00000";
  alias check_stable_start_event_1 : std_logic is check_stable_in_1(1);
  alias check_stable_end_event_1 : std_logic is check_stable_in_1(2);
  alias check_stable_expr_1 : std_logic_vector(2 downto 0) is check_stable_in_1(3 to 5);
  alias check_stable_start_event_2 : std_logic is check_stable_in_2(1);
  alias check_stable_end_event_2 : std_logic is check_stable_in_2(2);
  alias check_stable_expr_2 : std_logic_vector(2 downto 0) is check_stable_in_2(3 to 5);
  alias check_stable_start_event_3 : std_logic is check_stable_in_3(1);
  alias check_stable_end_event_3 : std_logic is check_stable_in_3(2);
  alias check_stable_expr_3 : std_logic_vector(2 downto 0) is check_stable_in_3(3 to 5);

  signal check_stable_start_event_4 : std_logic := '0';
  signal check_stable_end_event_4 : std_logic := '0';
  signal check_stable_expr_4 : std_logic_vector(7 to 9) := "000";

  signal check_stable_in_5, check_stable_in_6, check_stable_in_7 : std_logic_vector(1 to 3) := "000";
  alias check_stable_start_event_5 : std_logic is check_stable_in_5(1);
  alias check_stable_end_event_5 : std_logic is check_stable_in_5(2);
  alias check_stable_expr_5 : std_logic is check_stable_in_5(3);
  alias check_stable_start_event_6 : std_logic is check_stable_in_6(1);
  alias check_stable_end_event_6 : std_logic is check_stable_in_6(2);
  alias check_stable_expr_6 : std_logic is check_stable_in_6(3);
  alias check_stable_start_event_7 : std_logic is check_stable_in_7(1);
  alias check_stable_end_event_7 : std_logic is check_stable_in_7(2);
  alias check_stable_expr_7 : std_logic is check_stable_in_7(3);

  signal check_stable_en_1, check_stable_en_2, check_stable_en_3, check_stable_en_4 : std_logic := '1';
  signal check_stable_en_5, check_stable_en_6, check_stable_en_7 : std_logic := '1';

  shared variable check_stable_checker2, check_stable_checker3 : checker_t;
  shared variable check_stable_checker6, check_stable_checker7 : checker_t;
begin
  clock: process is
  begin
    while runner.phase < test_runner_exit loop
      clk <= '1', '0' after 5 ns;
      wait for 10 ns;
    end loop;
    wait;
  end process clock;

  check_stable_1 : check_stable(clk,
                                            check_stable_en_1,
                                            check_stable_start_event_1,
                                            check_stable_end_event_1,
                                            check_stable_expr_1);
  check_stable_2 : check_stable(check_stable_checker2,
                                            clk,
                                            check_stable_en_2,
                                            check_stable_start_event_2,
                                            check_stable_end_event_2,
                                            check_stable_expr_2,
                                            active_clock_edge => falling_edge);
  check_stable_3 : check_stable(check_stable_checker3,
                                            clk,
                                            check_stable_en_3,
                                            check_stable_start_event_3,
                                            check_stable_end_event_3,
                                            check_stable_expr_3);

  check_stable_4 : check_stable(clk,
                                            check_stable_en_4,
                                            check_stable_start_event_4,
                                            check_stable_end_event_4,
                                            check_stable_expr_4);

  check_stable_5 : check_stable(clk,
                                            check_stable_en_5,
                                            check_stable_start_event_5,
                                            check_stable_end_event_5,
                                            check_stable_expr_5);
  check_stable_6 : check_stable(check_stable_checker6,
                                            clk,
                                            check_stable_en_6,
                                            check_stable_start_event_6,
                                            check_stable_end_event_6,
                                            check_stable_expr_6,
                                            active_clock_edge => falling_edge);
  check_stable_7 : check_stable(check_stable_checker7,
                                            clk,
                                            check_stable_en_7,
                                            check_stable_start_event_7,
                                            check_stable_end_event_7,
                                            check_stable_expr_7);

  check_stable_runner : process
    variable pass : boolean;
    variable stat : checker_stat_t;

    procedure test_concurrent_std_logic_vector_check (
      signal clk                        : in  std_logic;
      signal check_input                : out std_logic_vector(1 to 5);
      variable checker : inout checker_t ;
      constant level                    : in  log_level_t := error;
      constant active_rising_clock_edge : in  boolean := true) is
    begin
      if running_test_case = "Test concurrent checker should pass stable window" then
        get_checker_stat(checker, stat);
        apply_sequence("00.101;10.101;00.101;01.101;00.101", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_passed_checks(checker, stat, 6);
      elsif running_test_case = "Test concurrent checker should pass window with varying drive strength" then
        get_checker_stat(checker, stat);
        apply_sequence("00.101;10.101;00.1LH;01.101;00.101", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_passed_checks(checker, stat, 6);
      elsif running_test_case = "Test concurrent checker should handle weak start and end events" then
        apply_sequence("00.101;HL.101;LL.111;LH.111;00.111", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(set_count(get_count + 2), expected_level => level);
      elsif running_test_case = "Test concurrent checker should fail unstable window" then
        apply_sequence("00.101;10.101;00.111;01.111;00.111", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(set_count(get_count + 2), expected_level => level);
      elsif running_test_case = "Test concurrent checker should fail window with weak changes to opposite level" then
        apply_sequence("00.101;10.101;00.L01;01.1H1;00.111", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(set_count(get_count + 2), expected_level => level);
      elsif running_test_case = "Test concurrent checker should fail on unknown start event" then
        apply_sequence("00.101;X0.101;00.111;01.101;00.101", clk, check_input, active_rising_clock_edge);
        verify_log_call(inc_count, "Unknown start event.", level);
      elsif running_test_case = "Test concurrent checker should fail on unknown end event in active window" then
        apply_sequence("00.101;0X.101;10.101;0X.101;00.101", clk, check_input, active_rising_clock_edge);
        verify_log_call(inc_count, "Unknown end event.", level);
      elsif running_test_case = "Test concurrent checker should fail on stable unknown window" then
        apply_sequence("00.101;10.10X;00.10X;01.10X;00.101", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(set_count(get_count + 3), "Unknown data in window.", level);
      elsif running_test_case = "Test concurrent checker should handle back to back windows" then
        apply_sequence("00.101;10.101;01.111;10.010", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(inc_count, expected_level => level);
        apply_sequence("10.010;01.101;00.101", clk, check_input, active_rising_clock_edge);
        verify_log_call(inc_count, expected_level => level);
      elsif running_test_case = "Test concurrent checker should ignore second of two overlapping windows" then
        apply_sequence("00.101;10.101;10.111;01.111;00.111;00.101;01.101;00.101", clk, check_input, active_rising_clock_edge);
        verify_log_call(set_count(get_count + 2), expected_level => level);
      elsif running_test_case = "Test concurrent checker should test one cycle windows" then
        get_checker_stat(checker, stat);
        apply_sequence("00.101;11.101;10.111;01.111;00.111", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_passed_checks(checker, stat, 6);
      end if;
    end procedure test_concurrent_std_logic_vector_check;

    procedure test_concurrent_std_logic_check (
      signal clk                        : in  std_logic;
      signal check_input                : out std_logic_vector(1 to 3);
      variable checker : inout checker_t ;
      constant level                    : in  log_level_t := error;
      constant active_rising_clock_edge : in  boolean := true) is
    begin
      if running_test_case = "Test concurrent checker should pass stable window" then
        get_checker_stat(checker, stat);
        apply_sequence("00.1;10.1;00.1;01.1;00.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_passed_checks(checker, stat, 6);
      elsif running_test_case = "Test concurrent checker should pass window with varying drive strength" then
        get_checker_stat(checker, stat);
        apply_sequence("00.1;10.1;00.H;01.1;00.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_passed_checks(checker, stat, 6);
      elsif running_test_case = "Test concurrent checker should handle weak start and end events" then
        apply_sequence("00.0;HL.0;LL.1;LH.1;00.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(set_count(get_count + 2), expected_level => level);
      elsif running_test_case = "Test concurrent checker should fail unstable window" then
        apply_sequence("00.0;10.0;00.1;01.1;00.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(set_count(get_count + 2), expected_level => level);
      elsif running_test_case = "Test concurrent checker should fail window with weak changes to opposite level" then
        apply_sequence("00.1;10.1;00.L;01.1;00.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(inc_count, expected_level => level);
      elsif running_test_case = "Test concurrent checker should fail on unknown start event" then
        apply_sequence("00.0;X0.0;00.1;01.0;00.0", clk, check_input, active_rising_clock_edge);
        verify_log_call(inc_count, "Unknown start event.", level);
      elsif running_test_case = "Test concurrent checker should fail on unknown end event in active window" then
        apply_sequence("00.1;0X.1;10.1;0X.1;00.1", clk, check_input, active_rising_clock_edge);
        verify_log_call(inc_count, "Unknown end event.", level);
      elsif running_test_case = "Test concurrent checker should fail on stable unknown window" then
        apply_sequence("00.1;10.X;00.X;01.X;00.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(set_count(get_count + 3), "Unknown data in window.", level);
      elsif running_test_case = "Test concurrent checker should handle back to back windows" then
        apply_sequence("00.0;10.0;01.1;10.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_log_call(inc_count, expected_level => level);
        apply_sequence("10.1;01.0;00.0", clk, check_input, active_rising_clock_edge);
        verify_log_call(inc_count, expected_level => level);
      elsif running_test_case = "Test concurrent checker should ignore second of two overlapping windows" then
        apply_sequence("00.0;10.0;10.1;01.1;00.1;00.0;01.0;00.0", clk, check_input, active_rising_clock_edge);
        verify_log_call(set_count(get_count + 2), expected_level => level);
      elsif running_test_case = "Test concurrent checker should test one cycle windows" then
        get_checker_stat(checker, stat);
        apply_sequence("00.0;11.0;10.1;01.1;00.1", clk, check_input, active_rising_clock_edge);
        wait for 1 ns;
        verify_passed_checks(checker, stat, 6);
      end if;
    end procedure test_concurrent_std_logic_check;

  begin
    custom_checker_init_from_scratch(check_stable_checker3, default_level => info);
    custom_checker_init_from_scratch(check_stable_checker7, default_level => info);
    test_runner_setup(runner, runner_cfg);

    while test_suite loop
      if run("Test concurrent checker should pass stable window") or
        run("Test concurrent checker should pass window with varying drive strength") or
        run("Test concurrent checker should handle weak start and end events") or
        run("Test concurrent checker should fail unstable window") or
        run("Test concurrent checker should fail window with weak changes to opposite level") or
        run("Test concurrent checker should fail on unknown start event") or
        run("Test concurrent checker should fail on unknown end event in active window") or
        run("Test concurrent checker should fail on stable unknown window") or
        run("Test concurrent checker should handle back to back windows") or
        run("Test concurrent checker should ignore second of two overlapping windows") or
        run("Test concurrent checker should test one cycle windows") then

        test_concurrent_std_logic_vector_check(clk, check_stable_in_1, default_checker);
        test_concurrent_std_logic_vector_check(clk, check_stable_in_2, check_stable_checker2, error, false);
        test_concurrent_std_logic_vector_check(clk, check_stable_in_3, check_stable_checker3, info);
        test_concurrent_std_logic_check(clk, check_stable_in_5, default_checker);
        test_concurrent_std_logic_check(clk, check_stable_in_6, check_stable_checker6, error, false);
        test_concurrent_std_logic_check(clk, check_stable_in_7, check_stable_checker7, info);
      elsif run("Test concurrent checker with std_logic_vector input should pass unstable window if not enabled") then
        wait until rising_edge(clk);
        wait for 1 ns;
        get_checker_stat(stat);
        apply_sequence("00.101;10.101;00.111", clk, check_stable_in_1);
        check_stable_en_1 <= '0';
        apply_sequence("00.111;01.101", clk, check_stable_in_1);
        check_stable_en_1 <= '1';
        apply_sequence("01.101;00.101", clk, check_stable_in_1);
        apply_sequence("00.101;10.101;00.111", clk, check_stable_in_1);
        check_stable_en_1 <= 'L';
        apply_sequence("00.111;01.101", clk, check_stable_in_1);
        check_stable_en_1 <= 'H';
        apply_sequence("01.101;00.101", clk, check_stable_in_1);
        apply_sequence("00.101;10.101;00.111", clk, check_stable_in_1);
        check_stable_en_1 <= 'X';
        apply_sequence("00.111;01.101", clk, check_stable_in_1);
        check_stable_en_1 <= '1';
        apply_sequence("01.101;00.101", clk, check_stable_in_1);
        wait until rising_edge(clk);
        wait for 1 ns;
        verify_passed_checks(stat, 12);
        verify_failed_checks(stat, 0);
      elsif run("Test concurrent checker with std_logic input should pass unstable window if not enabled") then
        wait until rising_edge(clk);
        wait for 1 ns;
        get_checker_stat(stat);
        apply_sequence("00.0;10.0;00.1", clk, check_stable_in_5);
        check_stable_en_5 <= '0';
        apply_sequence("00.1;01.0", clk, check_stable_in_5);
        check_stable_en_5 <= '1';
        apply_sequence("01.0;00.0", clk, check_stable_in_5);
        apply_sequence("00.0;10.0;00.1", clk, check_stable_in_5);
        check_stable_en_5 <= 'L';
        apply_sequence("00.1;01.0", clk, check_stable_in_5);
        check_stable_en_5 <= 'H';
        apply_sequence("01.0;00.0", clk, check_stable_in_5);
        apply_sequence("00.0;10.0;00.1", clk, check_stable_in_5);
        check_stable_en_5 <= 'X';
        apply_sequence("00.1;01.0", clk, check_stable_in_5);
        check_stable_en_5 <= '1';
        apply_sequence("01.0;00.0", clk, check_stable_in_5);
        wait until rising_edge(clk);
        wait for 1 ns;
        verify_passed_checks(stat, 12);
        verify_failed_checks(stat, 0);
      elsif run("Test should handle reversed and or offset expressions") then
        wait until rising_edge(clk);
        wait for 1 ns;
        get_checker_stat(stat);
        check_stable_start_event_4 <= '1';
        check_stable_expr_4 <= "101";
        wait until rising_edge(clk);
        check_stable_start_event_4 <= '0';
        wait until rising_edge(clk);
        check_stable_end_event_4 <= '1';
        wait until rising_edge(clk);
        check_stable_end_event_4 <= '0';
        wait for 1 ns;
        verify_passed_checks(stat, 6);
      end if;
    end loop;

    get_and_print_test_result(stat);
    test_runner_cleanup(runner, stat);
    wait;
  end process;

  test_runner_watchdog(runner, 4 us);

end test_fixture;

-- vunit_pragma run_all_in_same_sim
