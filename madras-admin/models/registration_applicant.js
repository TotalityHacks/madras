'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('registration_applicant', {
    'password': {
      type: DataTypes.STRING,
    },
    'last_login': {
      type: DataTypes.DATE,
    },
    'is_superuser': {
      type: DataTypes.BOOLEAN,
    },
    'first_name': {
      type: DataTypes.STRING,
    },
    'last_name': {
      type: DataTypes.STRING,
    },
    'is_staff': {
      type: DataTypes.BOOLEAN,
    },
    'is_active': {
      type: DataTypes.BOOLEAN,
    },
    'date_joined': {
      type: DataTypes.DATE,
    },
    'github_user_name': {
      type: DataTypes.STRING,
    },
    'email': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'registration_applicant',
    underscored: true,
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
  };

  return Model;
};

