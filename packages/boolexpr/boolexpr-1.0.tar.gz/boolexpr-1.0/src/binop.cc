// Copyright 2016 Chris Drake
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


#include <memory>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include <boost/optional.hpp>
#include <cryptominisat4/cryptominisat.h>

#include "boolexpr/boolexpr.h"


using namespace boolexpr;


bx_t
Atom::to_binop() const
{
    return shared_from_this();
}


static bx_t
_nop_to_binop(BoolExpr const * const bx)
{
    auto nop = bx->shared_from_this();
    auto op = ~nop;
    return ~op->to_binop();
}

bx_t Nor::to_binop() const { return _nop_to_binop(this); }
bx_t Nand::to_binop() const { return _nop_to_binop(this); }
bx_t Xnor::to_binop() const { return _nop_to_binop(this); }
bx_t Unequal::to_binop() const { return _nop_to_binop(this); }
bx_t NotImplies::to_binop() const { return _nop_to_binop(this); }
bx_t NotIfThenElse::to_binop() const { return _nop_to_binop(this); }


bx_t
Or::to_binop() const
{
    auto self = shared_from_this();
    auto op = std::static_pointer_cast<Operator const>(self);

    if (op->args.size() == 0)  // LCOV_EXCL_LINE
        return Or::identity(); // LCOV_EXCL_LINE

    if (op->args.size() == 1)           // LCOV_EXCL_LINE
        return op->args[0]->to_binop(); // LCOV_EXCL_LINE

    if (op->args.size() == 2)
        return transform([](bx_t const & bx){return bx->to_binop();});

    // x0 | x1 | x2 | x3 <=> (x0 | x1) | (x2 | x3)
    size_t const mid = op->args.size() / 2;

    auto lo = or_(vector<bx_t>(op->args.cbegin(), op->args.cbegin() + mid));
    auto hi = or_(vector<bx_t>(op->args.cbegin() + mid, op->args.cend()));

    return lo->to_binop() | hi->to_binop();
}


bx_t
And::to_binop() const
{
    auto self = shared_from_this();
    auto op = std::static_pointer_cast<Operator const>(self);

    if (op->args.size() == 0)   // LCOV_EXCL_LINE
        return And::identity(); // LCOV_EXCL_LINE

    if (op->args.size() == 1)           // LCOV_EXCL_LINE
        return op->args[0]->to_binop(); // LCOV_EXCL_LINE

    if (op->args.size() == 2)
        return transform([](bx_t const & bx){return bx->to_binop();});

    // x0 & x1 & x2 & x3 <=> (x0 & x1) & (x2 & x3)
    size_t const mid = op->args.size() / 2;

    auto lo = and_(vector<bx_t>(op->args.cbegin(), op->args.cbegin() + mid));
    auto hi = and_(vector<bx_t>(op->args.cbegin() + mid, op->args.cend()));

    return lo->to_binop() & hi->to_binop();
}


bx_t
Xor::to_binop() const
{
    auto self = shared_from_this();
    auto op = std::static_pointer_cast<Operator const>(self);

    if (op->args.size() == 0)   // LCOV_EXCL_LINE
        return Xor::identity(); // LCOV_EXCL_LINE

    if (op->args.size() == 1)           // LCOV_EXCL_LINE
        return op->args[0]->to_binop(); // LCOV_EXCL_LINE

    if (op->args.size() == 2)
        return transform([](bx_t const & bx){return bx->to_binop();});

    // x0 ^ x1 ^ x2 ^ x3 <=> (x0 ^ x1) ^ (x2 ^ x3)
    size_t const mid = op->args.size() / 2;

    auto lo = xor_(vector<bx_t>(op->args.cbegin(), op->args.cbegin() + mid));
    auto hi = xor_(vector<bx_t>(op->args.cbegin() + mid, op->args.cend()));

    return lo->to_binop() ^ hi->to_binop();
}


bx_t
Equal::to_binop() const
{
    auto self = shared_from_this();
    auto op = std::static_pointer_cast<Operator const>(self);

    if (op->args.size() < 2) // LCOV_EXCL_LINE
        return one();        // LCOV_EXCL_LINE

    if (op->args.size() == 2)
        return transform([](bx_t const & bx){return bx->to_binop();});

    size_t n = op->args.size();

    vector<bx_t> _args(n);
    for (size_t i = 0; i < n; ++i)
        _args[i] = args[i]->to_binop();

    vector<bx_t> pairs(n * (n-1) / 2);
    size_t cnt = 0;
    for (size_t i = 0; i < (n-1); ++i) {
        for (size_t j = i + 1; j < n; ++j)
            pairs[cnt++] = eq({_args[i], _args[j]});
    }

    return and_(std::move(pairs));
}


bx_t
Implies::to_binop() const
{
    return transform([](bx_t const & bx){return bx->to_binop();});
}


bx_t
IfThenElse::to_binop() const
{
    return transform([](bx_t const & bx){return bx->to_binop();});
}
