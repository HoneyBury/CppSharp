#include <gtest/gtest.h>

#include "cppsharp/my_lib.hpp"

class MyLibTest : public ::testing::Test
{
   protected:
    void SetUp() override
    {
        setup_logger();
    }
};

TEST_F(MyLibTest, GreetFunction)
{
    ASSERT_NO_THROW(greet("Tester"));
}

TEST(MyLibStandaloneTest, AlwaysPass)
{
    EXPECT_EQ(1, 1);
    ASSERT_TRUE(true);
}
