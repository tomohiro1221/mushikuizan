class Multiplication():
    def __init__(self, first, second, rows, answer, env=None):
        assert len(second) == len(rows)
        if env is None:
            self.first = list(first)
            self.second = list(second)
            self.rows = [list(row) for row in rows]
            self.answer = list(answer)
        else:
            f = self.get_full_row_int(first, env["first"])
            s = self.get_full_row_int(second, env["second"])
            self.first = list(str(f))
            self.second = list(str(s))
            self.rows = []
            for c in reversed(str(s)):
                self.rows.append(list(str(int(c) * f)))
            self.answer = list(str(f * s))
        self.nb_col = len(self.answer)

    def __str__(self):
        """
        Returns:
            multiplication in str

        Examples:
            >>> mul = Multiplication('x7x', 'x5', ['xx9x', '1x56'], '16xxx')
            >>> print mul
                       X01    7  X02
                            X03    5
            -------------------------
                  X04  X05    9  X06
               1  X07    5    6
            -------------------------
               1    6  X08  X09  X10
        """
        s = ''
        counter = 0
        row_str, counter = self.get_row_str(self.first, counter, 0)
        s += row_str
        row_str, counter = self.get_row_str(self.second, counter, 0)
        s += row_str
        s += (5 * self.nb_col) * "-"
        s += '\n'
        for i, row in enumerate(self.rows):
            row_str, counter = self.get_row_str(row, counter, i)
            s += row_str
        s += (5 * self.nb_col) * "-"
        s += '\n'
        row_str, counter = self.get_row_str(self.answer, counter, 0)
        s += row_str
        return s

    def get_row_str(self, row, counter, shift):
        """
        Args:
            row: a list of characters consisting of '0', '1', ... '9', or 'x'
            counter: the number of 'x'es in rows above
            shift: the length of padding in the left

        Returns:
            s: row converted to str
            counter: the number of encountered 'x'es so far
        """
        s = ''
        row_str = ['' for _ in range(self.nb_col - len(row) - shift)] + row + list(shift * '')
        for c in row_str:
            if c == 'x':
                counter += 1
                s += '{:>4}'.format("X" + "{:02}".format(counter))
            else:
                s += '{:>4}'.format(c)
            s += ' '
        s += '\n'
        return s, counter

    def configurable_env(self):
        """
        Returns:
            a hash h where h["first" or "second"][an index at which "first" or "second" row is 'x'] is None
        """
        return {"first": {i: None for i, c in enumerate(self.first) if c == 'x'},
                "second": {i: None for i, c in enumerate(self.second) if c == 'x'}}

    @staticmethod
    def get_full_row_int(row, row_env):
        """
        Args:
            row: a list of characters consisting of '0', '1', ... '9', or 'x'
            row_env: environment that substitutes 'x' in row

        Returns:
            the largest available integer available in the row with row_env applied.

        Raises:
            ValueError: if 'x' in row is not supplemented by row_env and unknown
        """
        a = 0
        for i, c in enumerate(row):
            a *= 10
            if c == 'x':
                if row_env[i] is not None:
                    a += row_env[i]
                else:
                    raise ValueError("Evaluating a row with an incomplete environment.")
            else:
                a += int(c)
        return a

    @staticmethod
    def get_partial_row_int(row, row_env):
        """
        Args:
            row: a list of characters consisting of '0', '1', ... '9', or 'x'
            row_env: environment that substitutes 'x' in row

        Returns:
            the largest available integer available in the row with row_env applied.

        Examples:
            >>> mul.get_partial_row_int(['x', '7', 'x'], {0: None, 2: None})
            None

            >>> mul.get_partial_row_int(['x', '7', 'x'], {0: None, 2: 5}
            75

            >>> mul.get_partial_row_int(['x', '7', 'x'], {0: 1, 2: 5}
            175
        """
        if row[-1] == 'x' and row_env[len(row)-1] is None:
            return None
        a = 0
        for i, c in enumerate(row):
            a *= 10
            if c == 'x':
                if row_env[i] is not None:
                    a += row_env[i]
                else:
                    a = 0
            else:
                a += int(c)
        return a

    @staticmethod
    def match_rows(r1, r2, full=False):
        """
        Args:
            r1: a list of characters consisting of '0', '1', ... '9', or 'x'
            r2: a list of characters consisting of '0', '1', ... '9'
            full: if True, r1 and r2 have to be fully matched

        Returns:
            True if r1 and r2 matches, False otherwise
        """
        if full and len(r1) != len(r2):
            return False
        for c1, c2 in zip(r1, r2):
            if c1 == 'x' or c1 == c2:
                continue
            else:
                return False
        return True

    def is_sufficient(self, env):
        """
        Args:
            env: a hash environment

        Returns:
            False if "nogood" True otherwise
        """
        if env["first"].get(0) == 0 or env["second"].get(0) == 0:
            return False

        first_row = self.get_partial_row_int(self.first, env["first"])
        if first_row is None:
            return True

        for i, (a, row) in enumerate(zip(self.second, reversed(self.rows))):
            if a == 'x':
                if env["second"].get(i) is None:
                    continue
                else:
                    a = env["second"][i]
            else:
                a = int(a)
            evaluated_row = str(first_row * a)
            if len(str(first_row)) == len(self.first):
                if not self.match_rows(row, evaluated_row, full=True):
                    return False
            else:
                # The following line extracts the only relevant part of the row.
                # For instance, when first_row is 70 and a is 5, evaluated_row becoming 350,
                # the leftmost digit in evaluated_row '3' is a carry out,
                # and isn't an actual result of multiplication, and thus dropped.
                relevant = evaluated_row[-len(str(first_row)):]
                if not self.match_rows(row[-len(relevant):], relevant):
                    return False

        if all([v is not None for v in env["first"].values()]) and \
                all([v is not None for v in env["second"].values()]):
            first = self.get_full_row_int(self.first, env["first"])
            second = self.get_full_row_int(self.second, env["second"])
            answer = str(first * second)
            if not self.match_rows(self.answer, answer, full=True):
                return False
        return True
